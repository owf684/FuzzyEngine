import sys
sys.path.append("./LevelEditor/components")
import object_creator_component
import editor_ui_component

class LevelEditor:

    def __init__(self):

        # setup object creator
        self.c_object_creator = object_creator_component.ObjectCreatorComponent()
        self.c_object_creator.s_directory_path ='./GameData/jsons'
        self.c_object_creator.create_json_list()
        self.c_object_creator.create_objects_dict()
        self.c_object_creator.organize_objects()

        # setup editor ui
        self.editor_ui = editor_ui_component.EditorUIComponent()
        self.editor_ui.init_ui(self.c_object_creator)

        # input latch bools
        self.arrow_hori_latch = False
        self.arrow_vert_latch = False

    def main(self,**kwargs):
        d_inputs=kwargs['InputDict']
        l_render_buffer=kwargs['RenderBuffer']

        self.handle_inputs(d_inputs)
        return self.editor_ui.ui_elements
    


    def handle_inputs(self,d_inputs):
        self.category_handler(d_inputs)



    def category_handler(self,d_inputs):

        if d_inputs['arrow-vert'] == 1 and not self.arrow_vert_latch:
            self.arrow_vert_latch = True
            self.c_object_creator.i_category += 1
        elif d_inputs['arrow-vert'] == -1 and not self.arrow_vert_latch:
            self.arrow_vert_latch = True
            self.c_object_creator.i_category -= 1
        elif d_inputs['arrow-vert'] == 0 and self.arrow_vert_latch:
            self.arrow_vert_latch = False

        if d_inputs['arrow-vert'] == 1 and not self.arrow_hori_latch:
            self.arrow_hori_latch = True
            self.c_object_creator.i_object += 1
        elif d_inputs['arrow-vert'] == -1 and not self.arrow_hori_latch:
            self.arrow_hori_latch = True
            self.c_object_creator.i_object -= 1
        elif d_inputs['arrow-vert'] == 0 and self.arrow_hori_latch:
            self.arrow_hori_latch = False
        
        i_category = self.c_object_creator.i_category
        i_object = self.c_object_creator.i_object

        print(self.c_object_creator.i_category)
        print(self.c_object_creator.i_object)

        # clamp category and object indicies
        print(len(self.c_object_creator.l_categories))
        if self.c_object_creator.i_category >= len(self.c_object_creator.l_categories):
            self.c_object_creator.i_category = len(self.c_object_creator.l_categories) -1
        elif self.c_object_creator.i_category < 0:
            self.c_object_creator.i_category = 0

        if self.c_object_creator.i_object >= len(self.c_object_creator.l_categories[i_category]):
            self.c_object_creator.i_object = len(self.c_object_creator.l_categories[i_category]) -1
        elif self.c_object_creator.i_object < 0:
            self.c_object_creator.i_object = 0

        print(self.c_object_creator.i_category)
        print(self.c_object_creator.i_object)

