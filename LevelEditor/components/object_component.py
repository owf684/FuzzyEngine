import pygame
import sys
import json
import os

sys.path.append("./Objects/components")
sys.path.append("./Objects/Templates")
import object_template
import text_box_ui_component
import combo_box_ui_component
from vector import Vector
from form import Form

class ObjectComponent:

    def __init__(self):
        # read in current project directory
        with open('./project_file.json', 'r') as file:
            self.project_file = json.load(file)

        self.display_info = pygame.display.Info()
        self.display_width = int(self.display_info.current_w * .8)
        self.display_height = int(self.display_info.current_h * .8)
        self.font = pygame.font.Font(None, 24)
        self.font_color = (255, 255, 255)

        self.generic_1_sprite_is_sheet = False
        self.generic_2_sprite_is_sheet = False
        self.generic_3_sprite_is_sheet = False
        self.generic_4_sprite_is_sheet = False
        self.file_collection = {}

        self.selected_index = {'current_sprite_dir': -1,
                               'generic_sprite_1_dir': -1,
                               'generic_sprite_2_dir': -1,
                               'generic_sprite_3_dir': -1,
                               'generic_sprite_4_dir': -1}

        self.f_object_component = Form(25, 10, self.display_width * .95, self.display_height * .95)
        self.setup_object_component_form()
        self.level_editor = None
    def setup_object_component_form(self):

        # Setting up Labels
        y_pos = 50
        y_increment = 75
        # add 4 labels
        label_text = {'l1': 'Current Sprite',
                      'l2': 'Generic Sprite 1',
                      'l3': 'Generic Sprite 2',
                      'l4': 'Generic Sprite 3',
                      'l5': 'Generic Sprite 4',
                      'l6': 'Object Class',
                      'l7': 'Object Category'}

        for key, label in label_text.items():
            self.f_object_component.add_label(key, label, 100, y_pos, 24)
            y_pos += y_increment

        # Setting up sprite directory combo boxes
        y_pos = 45
        combo_boxes = {'current_sprite_dir': 'None',
                       'generic_sprite_1_dir': 'None',
                       'generic_sprite_2_dir': 'None',
                       'generic_sprite_3_dir': 'None',
                       'generic_sprite_4_dir': 'None'}
        for key, combo in combo_boxes.items():
            self.f_object_component.add_combo_box(key,300,y_pos,200,25)
            self.f_object_component.combo_boxes[key].add_entry(combo)
            self.f_object_component.combo_boxes[key].connect(self.update_form_combo_boxes, True)
            y_pos += y_increment


        # Setting up sprite file combo boxes
        y_pos = 45
        combo_boxes = {'current_sprite_file': 'None',
                       'generic_sprite_1_file': 'None',
                       'generic_sprite_2_file': 'None',
                       'generic_sprite_3_file': 'None',
                       'generic_sprite_4_file': 'None'}
        for key, combo in combo_boxes.items():
            self.f_object_component.add_combo_box(key,550,y_pos,200,25)
            self.f_object_component.combo_boxes[key].add_entry(combo)
            y_pos += y_increment


        # Setting up sprite sheet switches
        y_pos = 45 + y_increment
        switches = {'generic_switch_1': 'sprite sheet',
                    'generic_switch_2': 'sprite sheet',
                    'generic_switch_3': 'sprite sheet',
                    'generic_switch_4': 'sprite sheet'}
        for key, switches in switches.items():
            self.f_object_component.add_switch(key,switches,800,y_pos,100, 25)
            y_pos += y_increment

        # Setting up object class entry
        y_pos = 45 + y_increment*5
        self.f_object_component.add_entry('object_class',300,y_pos, 200, 25,18)

        # Setting up object category combo box
        y_pos = 45 + y_increment*6
        self.f_object_component.add_combo_box('object_category',300,y_pos, 200, 25)
        self.f_object_component.combo_boxes['object_category'].add_entry('environment_object')
        self.f_object_component.combo_boxes['object_category'].add_entry('player_object')
        self.f_object_component.combo_boxes['object_category'].add_entry('item_object')
        self.f_object_component.combo_boxes['object_category'].add_entry('scene_object')
        self.f_object_component.combo_boxes['object_category'].add_entry('enemy_object')

        # Setting up Save Button
        y_pos = 45 + y_increment*6
        self.f_object_component.add_button('save_object', 'SAVE', 550, y_pos, 200, 50)
        self.f_object_component.buttons['save_object'].font_size = 24
        self.f_object_component.buttons['save_object'].font = pygame.font.Font(None, 24)
        self.f_object_component.buttons['save_object'].set_text('SAVE')
        self.f_object_component.buttons['save_object'].connect(self.save_object)

        # Setting up Cancel Button
        y_pos = 45 + y_increment*6
        self.f_object_component.add_button('cancel', 'CANCEL', 800, y_pos, 200, 50)
        self.f_object_component.buttons['cancel'].font_size = 24
        self.f_object_component.buttons['cancel'].font = pygame.font.Font(None, 24)
        self.f_object_component.buttons['cancel'].set_text('CANCEL')
        self.f_object_component.buttons['cancel'].connect(self.cancel)

        # Initialize combo box entries
        self.find_sprites()
        #self.find_sprites_new()
    def update(self, **kwargs):
        self.level_editor = kwargs['LevelEditor']
        # self.update_form_combo_boxes()
        self.update_sprite_sheet_status()

    def update_form_combo_boxes(self, **kwargs):

        dir_cb_key = kwargs['name']

        if dir_cb_key is not None:

            selected_dir = self.f_object_component.combo_boxes[dir_cb_key].get_value()
            file_cb_key = dir_cb_key[:dir_cb_key.index('dir')] + 'file'

            if selected_dir != 'None':
                self.f_object_component.combo_boxes[file_cb_key].reset()
                for entry in self.file_collection[selected_dir]:
                    self.f_object_component.combo_boxes[file_cb_key].add_entry(entry)

    def update_sprite_sheet_status(self):
        self.generic_1_sprite_is_sheet = self.f_object_component.switches['generic_switch_1'].is_toggled()
        self.generic_2_sprite_is_sheet = self.f_object_component.switches['generic_switch_2'].is_toggled()
        self.generic_3_sprite_is_sheet = self.f_object_component.switches['generic_switch_3'].is_toggled()
        self.generic_4_sprite_is_sheet = self.f_object_component.switches['generic_switch_4'].is_toggled()


    def find_sprites(self):
        self.file_collection.clear()
        for key, cb in self.f_object_component.combo_boxes.items():
            cb.reset()

        # walk through GameData directory
        for root, dirs, files in os.walk(self.project_file['current_project'] + '/GameData/Assets/'):
            game_data_index = root.index('/GameData')
            game_data_path = root[game_data_index:]
            png_files = list()
            for pngs in files:
                if 'png' in pngs:
                    png_files.append(pngs)

            if len(png_files) > 0:
                self.file_collection[game_data_path] = png_files
        for key, cb in self.f_object_component.combo_boxes.items():
            if 'dir' in key:
                for key, dir in self.file_collection.items():
                    cb.add_entry(key)

    def cancel(self):
        self.f_object_component.render = False
        self.level_editor.object_placer.place_enabled = True

    def save_object(self):

        current_sprite = self.f_object_component.combo_boxes['current_sprite_dir'].get_value()  + \
                         self.f_object_component.combo_boxes['current_sprite_file'].get_value()
        generic_sprite_1 = self.f_object_component.combo_boxes['generic_sprite_1_dir'].get_value()  + \
                           self.f_object_component.combo_boxes['generic_sprite_1_file'].get_value()
        generic_sprite_2 = self.f_object_component.combo_boxes['generic_sprite_2_dir'].get_value()  + \
                           self.f_object_component.combo_boxes['generic_sprite_2_file'].get_value()
        generic_sprite_3 = self.f_object_component.combo_boxes['generic_sprite_3_dir'].get_value()  + \
                           self.f_object_component.combo_boxes['generic_sprite_3_file'].get_value()
        generic_sprite_4 = self.f_object_component.combo_boxes['generic_sprite_4_dir'].get_value()  + \
                           self.f_object_component.combo_boxes['generic_sprite_4_file'].get_value()

        object_class = self.f_object_component.entries['object_class'].get_text()
        object_category = self.f_object_component.combo_boxes['object_category'].get_value()

        file_directory = "/GameData/" + object_template.object_categories[object_category] + 's'
        class_name = ''
        file_name = ''
        makeUpper = True
        uppersFound = 0

        # Convert class_name => ClassName
        if '_' in object_class:
            file_name = object_class.lower()
            for characters in object_class:
                if makeUpper and '_' not in characters:
                    class_name += characters.upper()
                    makeUpper = False
                elif '_' not in characters:
                    class_name += characters

                if characters == '_':
                    makeUpper = True
            object_class = class_name

        else:
            # convert ClassName => class_name
            for characters in object_class:

                if characters == characters.upper():
                    if uppersFound > 0:
                        file_name += '_'
                    file_name += characters.lower()
                    uppersFound += 1
                else:
                    file_name += characters
        file_name += '.py'

        # update file template
        file_template = object_template.get_file_template()
        file_template['parent_object'] = "import " + object_category
        file_template['class_define'] = 'class ' + object_class + '(' + object_category + "." + \
                                        object_template.object_categories[object_category] + "):"

        if 'None' not in current_sprite:
            file_template[
                'current_sprite'] = "self.current_sprite.create_sprite(project_dir + '" + current_sprite + "')"
        else:
            file_template.pop('current_sprite')

        if 'None' not in generic_sprite_1:
            if self.generic_1_sprite_is_sheet:
                file_template['generic_sprite_1'] = (
                    "self.generic_sprite_1.create_sprite_sheet(project_dir + '" + generic_sprite_1, 1,
                    Vector(32, 32))

            else:
                file_template[
                    'generic_sprite_1'] = "self.generic_sprite_1.create_sprite(project_dir + '" + generic_sprite_1 + '")'
                file_template.pop('generic_sprite_1_position')
                file_template.pop("generic_sprite_1_rect")
        else:
            file_template.pop("generic_sprite_1")
            file_template.pop('generic_sprite_1_position')
            file_template.pop("generic_sprite_1_rect")
        if 'None' not in generic_sprite_2:
            if self.generic_2_sprite_is_sheet:
                file_template['generic_sprite_2'] = (
                    "self.generic_sprite_2.create_sprite_sheet(project_dir + '" + generic_sprite_2, 1,
                    Vector(32, 32))

            else:
                file_template[
                    'generic_sprite_2'] = "self.generic_sprite_2.create_sprite(project_dir + '" + generic_sprite_2 + "')"
                file_template.pop('generic_sprite_2_position')
                file_template.pop("generic_sprite_2_rect")
        else:
            file_template.pop("generic_sprite_2")
            file_template.pop('generic_sprite_2_position')
            file_template.pop("generic_sprite_2_rect")
        if 'None' not in generic_sprite_3:
            if self.generic_3_sprite_is_sheet:
                file_template['generic_sprite_3'] = (
                    "self.generic_sprite_3.create_sprite_sheet(project_dir + '" + generic_sprite_3, 1,
                    Vector(32, 32))

            else:
                file_template[
                    'generic_sprite_3'] = "self.generic_sprite_3.create_sprite(project_dir + '" + generic_sprite_3 + "')"
                file_template.pop('generic_sprite_3_position')
                file_template.pop("generic_sprite_3_rect")
        else:
            file_template.pop("generic_sprite_3")
            file_template.pop('generic_sprite_3_position')
            file_template.pop("generic_sprite_3_rect")

        if 'None' not in generic_sprite_4:
            if self.generic_4_sprite_is_sheet:
                file_template['generic_sprite_4'] = (
                    "self.generic_sprite_4.create_sprite_sheet(project_dir + ' " + generic_sprite_4, 1,
                    Vector(32, 32))

            else:
                file_template[
                    'generic_sprite_4'] = "self.generic_sprite_4.create_sprite(project_dir + '" + generic_sprite_4 + "')"
                file_template.pop('generic_sprite_4_position')
                file_template.pop("generic_sprite_4_rect")

        else:
            file_template.pop("generic_sprite_4")
            file_template.pop('generic_sprite_4_position')
            file_template.pop("generic_sprite_4_rect")

        file_template[
            'object_json_file'] = "self.save_state.object_json_file='" + "/GameData/jsons/" + file_name.rstrip(
            '.py') + ".json'"

        file_template['object_return'] = "return " + object_class + "()"

        object_template.create_object_file(file_directory, file_name, file_template)

        # create object json 
        object_json = {
            "object_directory": file_directory,
            "object_file": file_name,
            "object_class": object_class,
            "object_category": object_category
        }
        with open(self.project_file['current_project'] + "/GameData/jsons/" + file_name.rstrip('.py') + ".json",
                  'w') as json_file:
            json.dump(object_json, json_file)


        self.f_object_component.render = False

        self.level_editor.c_object_creator.reset()
        self.level_editor.c_object_creator.create_json_list()
        self.level_editor.c_object_creator.create_objects_dict()
        self.level_editor.c_object_creator.organize_objects()
        self.level_editor.object_container_ui.init_ui(self.level_editor.c_object_creator)
