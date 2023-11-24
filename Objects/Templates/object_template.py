

file_template = {
    'sys_import': "import sys",
    'objects_path_append': "sys.path.append('./Objects')",
    'objects_components_path_append' : "sys.path.append('./Objects/components')",
    'parent_object': "import template_object",
    'class_define': "class userClass(template_object.TemplateObject):",
    'def_init' : "def __init__(self):",
    'super_init': "super().__init__()",
    'current_sprite': "self.current_sprite.create_sprite('./GameData/Assets/userDirectory')",
    'generic_sprite_1': "self.generic_sprite_1.create_sprite('./GameData/Assets/userDirectory')",
    'generic_sprite_2': "self.generic_sprite_2.create_sprite('./GameData/Assets/userDirectory')",
    'generic_sprite_3': "self.generic_sprite_3.create_sprite('./GameData/Assets/userDirectory')",
    'generic_sprite_4': "self.generic_sprite_4.create_sprite('./GameData/Assets/userDirectory')",
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
    'scene_object': 'SceneObject'
}

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
            object_file.write(indent + value + end_line)

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
        
