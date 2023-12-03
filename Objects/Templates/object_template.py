import sys
from copy import deepcopy

sys.path.append("./Objects/components")
from vector import Vector

file_template = {
    'sys_import': "import sys",
    'objects_path_append': "sys.path.append('./Objects')",
    'objects_components_path_append' : "sys.path.append('./Objects/components')",
    'parent_object': "import template_object",
    'vector_object': "from vector import Vector",
    'class_define': "class userClass(template_object.TemplateObject):",
    'def_init' : "def __init__(self):",
    'super_init': "super().__init__()",
    'current_sprite': "self.current_sprite.create_sprite('./GameData/Assets/userDirectory')",
    'generic_sprite_1': "self.generic_sprite_1.create_sprite_sheet('None',2,Vector(32,32))",
    'generic_sprite_1_position': 'self.generic_sprite_1.position = Vector(0,0)',
    'generic_sprite_1_rect': 'self.generic_sprite_1.create_sprite_sheet_rect()',
    'generic_sprite_2': "self.generic_sprite_2.create_sprite_sheet('./GameData/Assets/userDirectory')",
    'generic_sprite_2_position': 'self.generic_sprite_2.position = Vector(0,0)',
    'generic_sprite_2_rect': 'self.generic_sprite_2.create_sprite_sheet_rect()',
    'generic_sprite_3': "self.generic_sprite_3.create_sprite_sheet('./GameData/Assets/userDirectory')",
    'generic_sprite_3_position': 'self.generic_sprite_3.position = Vector(0,0)',
    'generic_sprite_3_rect': 'self.generic_sprite_3.create_sprite_sheet_rect()',
    'generic_sprite_4': "self.generic_sprite_4.create_sprite_sheet('./GameData/Assets/userDirectory')",
    'generic_sprite_4_position': 'self.generic_sprite_4.position = Vector(0,0)',
    'generic_sprite_4_rect': 'self.generic_sprite_4.create_sprite_sheet_rect()',
    'physics_pause': "self.physics.pause = True",
    'object_json_file': "self.save_state.object_json_file='./GameData/jsons/template_object.json'" ,
    "end_of_class": True,
    'def_create_object': "def create_object():",
    'object_return': "return userClass()",
    'end_of_function': True
}

object_categories ={
    'environment_object': 'EnvironmentObject',
    'game_object': 'GameObject',
    'item_object': 'ItemObject',
    'scene_object': 'SceneObject',
    'enemy_object': 'EnemyObject'
}
def get_file_template():
    return deepcopy(file_template)

def create_object_file(object_file_path,file_name,template):
    if object_file_path[-1] != '/':
        object_file_path += '/'
    object_file = open( object_file_path + file_name,"w")
    indent = ''
    end_line = '\n'
    class_indented = False
    def_indented = False
    for key, value in template.items():
        
        if 'end_of' not in key:
            if isinstance(value,str):
                object_file.write(indent + value + end_line)
            elif isinstance(value,tuple) and 'generic_sprite' in key:
                object_file.write(indent + str(value[0]) + "' , " + str(value[1]) + "," + str(Vector(value[2].x,value[2].y)) + ")" + end_line)

        if 'class' in key and not class_indented:
            indent ='\t'

        if 'def' in key and class_indented:
            indent += '\t'

        if 'def' in key and not def_indented:
            indent += '\t'
            
        if key == 'end_of_class' and value is True:
            indent = ''
        if key == 'end_of_function' and value is True:
            indent = ''

    object_file.close()
        
