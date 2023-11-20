import sys
sys.path.append('./Objects')
sys.path.append('./Objects/components')
import template_object # set by category

class userClass(template_object.TemplateObject): # set by userClass, set by category
		def __init__(self):
			super().__init__()
			self.current_sprite.create_sprite('./GameData/Assets/userDirectory') # set by sprite
			self.physics.pause = True
			self.save_state.object_json_file='./GameData/jsons/template_object.json'	# set by object_component

def create_object():
	return userClass() # set by userClass
