import json
import sys
import os
import failed_module_load

''' Hungarian notation
l = list()
d = dict()
s = str()
i = int()
'''
'''
ObjectCreator Intended Use:
The object creators ultimate goal is to create a list called l_categories.
This is a multidimensional list containing categories of different objects.
This list should make the traversal of objects and categories easy and is needed for 
the level editor. The level editor will use list l_categories and indicies i_category and i_object
to traverse l_categories.

example of what l_categories will look like

l_categories = 	[

		[object_1,category_1],[object_2,category_1],[object_3,category_1],

		[object_1,category_2],[object_2,category_2],[object_3,category_2],

		[object_1,category_3],[object_2,category_3],[object_3,category_3],

		]


'''
class ObjectCreatorComponent:

	def __init__(self):
		self.l_json_modules = list()
		self.l_objects = list()
		self.d_modules = {}
		self.s_directory_path = './GameData/jsons/'
		self.l_categories = list()
		self.i_category = 0
		self.i_object = 0
		self.update_editor_ui = False

	def reset(self):
		self.l_json_modules.clear()
		self.l_objects.clear()
		self.d_modules = {}
		self.l_categories.clear()
		self.i_category = 0
		self.i_object = 0
		self.update_editor_ui = False		
		
	def create_json_list(self,directory_path='./GameData/jsons/'):
		for root, dirs, files in os.walk(directory_path):
			for json_file in files:
				file_extension = os.path.splitext(json_file)[1]
				if file_extension.lower() == '.json':
					self.l_json_modules.append(os.path.join(root,json_file))
		print(len(self.l_json_modules))
					
	def create_objects_dict(self):	
		for json_module in self.l_json_modules:
		
			with open(json_module,'r') as json_file:
				module_data = json.load(json_file)
			try:
				sys.path.append(module_data['object_directory'])
				module_name = module_data['object_file'].rstrip(".py")
				category = module_data['object_category']
				self.d_modules[module_name] = __import__(module_name)
				self.l_objects.append([self.d_modules[module_name].create_object(),module_name,category])
	
			except Exception as Error:
				print("unable to create object: ", Error)

	def organize_objects(self):
		i = 0
		A = self.l_objects
		while i < len(A):
			temp_list = list()
			temp_list.append([A[i][0],A[i][1]])
			k = i + 1
			while k < len(A):
				if A[i][2] == A[k][2]:
					temp_list.append([A[k][0],A[k][1]]) 
					A.remove(A[k])
				else:
					k += 1
			self.l_categories.append(temp_list)
			i += 1

	def category_handler(self,d_inputs):
		if d_inputs["arrow_vert_latch"] or d_inputs["arrow_hori_latch"]:
			self.update_editor_ui = True
			
		if d_inputs['arrow-vert'] == 1 and not d_inputs["arrow_vert_latch"]:
			d_inputs["arrow_vert_latch"] = True
			self.i_category += 1
		elif d_inputs['arrow-vert'] == -1 and not d_inputs["arrow_vert_latch"]:
			d_inputs["arrow_vert_latch"] = True
			self.i_category -= 1
		elif d_inputs['arrow-vert'] == 0 and d_inputs["arrow_vert_latch"]:
			d_inputs["arrow_vert_latch"] = False
		if d_inputs['arrow-hori'] == 1 and not d_inputs["arrow_hori_latch"]:
			d_inputs["arrow_hori_latch"] = True
			self.i_object += 1		
		elif d_inputs['arrow-hori'] == -1 and not d_inputs["arrow_hori_latch"]:
			d_inputs["arrow_hori_latch"] = True
			self.i_object -= 1
		elif d_inputs['arrow-hori'] == 0 and d_inputs["arrow_hori_latch"]:
			d_inputs["arrow_hori_latch"] = False
                
		if self.i_category >= len(self.l_categories):
			self.i_category = len(self.l_categories) -1
		elif self.i_category < 0:
			self.i_category = 0

		if self.i_object >= len(self.l_categories[self.i_category]):
			self.i_object = len(self.l_categories[self.i_category]) -1
		elif self.i_object < 0:
			self.i_object = 0

	def reset(self):
		self.l_json_modules = list()
		self.l_objects = list()
		self.d_modules = {}
		self.s_directory_path = './'
		self.l_categories = list()

	def get_selected_category(self):
		return self.l_categories[self.i_category]
	
	def get_selected_object(self):
		return self.l_categories[self.i_category][self.i_object]
	
	def create_selected_object(self):
		module_name = self.l_categories[self.i_category][self.i_object][1]
		return self.d_modules[module_name].create_object() 
	
	def create_new_object(self,json_module):
		try:

			with open(json_module,'r') as json_file:
				module_data = json.load(json_file)
			module_name = module_data['object_file'].rstrip(".py")
			module = __import__(module_name)
			return module.create_object()
		except Exception as Error:
			return failed_module_load.create_object()
			
	def destroy_selected_object(self):
		selected_object = self.get_selected_object()[1]
		print(selected_object)
		reset_ui = False
		for root, dirs, files in os.walk("./"):
			for file in files:
				if selected_object in file and (".py" in file or ".json" in file) and not '.pyc' in file and "failed_module_load" not in file:
					os.remove(root+"/"+file)
					reset_ui = True

		if reset_ui:
			self.i_category = 0
			self.i_object = 0
			return True

		else:
			return False
