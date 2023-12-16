import json
import sys
import pygame

sys.path.append("./LevelEditor/components")
sys.path.append("./Objects/components")
import object_creator_component
import object_container_ui_component
import button_ui_component
import grid_ui_component
import tool_bar_ui_component
import attribute_ui_component
import object_placer_component
import text_box_ui_component
import scene_component
import object_component
import combo_box_ui_component
from vector import Vector


class LevelEditor:

    def __init__(self):
        # get display info
        self.display_info = pygame.display.Info()
        self.screen_width = int(self.display_info.current_w * .8)
        self.screen_height = int(self.display_info.current_h * .8)

        # setup object creator
        self.c_object_creator = object_creator_component.ObjectCreatorComponent()
        with open('project_file.json','r') as file:
            self.project_file = json.load(file)

        self.c_object_creator.s_directory_path = self.project_file['current_project']
        self.c_object_creator.create_json_list()
        self.c_object_creator.create_objects_dict()
        self.c_object_creator.organize_objects()

        # set up scene component
        self.c_scene = scene_component.SceneComponent()
        self.c_scene.get_scene_previews()

        # setup grid component
        self.grid = grid_ui_component.GridUIComponent()

        # setup tool bar
        self.tool_bar = tool_bar_ui_component.ToolBarUIComponent()

        # setup editor ui
        self.object_container_ui = object_container_ui_component.ObjectContainerUIComponent()
        self.object_container_ui.init_ui(self.c_object_creator)

        # setup object compoent
        self.c_object = object_component.ObjectComponent()

        # setup inspector buttons
        self.play_pause_button = button_ui_component.ButtonUIComponent()
        self.back_button = button_ui_component.ButtonUIComponent()
        self.add_object_button = button_ui_component.ButtonUIComponent()
        self.remove_object_button = button_ui_component.ButtonUIComponent()
        self.collision_button = button_ui_component.ButtonUIComponent()
        self.grid_move_switch = button_ui_component.ButtonUIComponent(switch=True)
        self.reload_objects_button = button_ui_component.ButtonUIComponent()

        self.scroll_in_edit = False

        # setup scene buttons
        self.add_scene_button = button_ui_component.ButtonUIComponent()
        self.save_scene_button = button_ui_component.ButtonUIComponent()
        self.delete_scene_button = button_ui_component.ButtonUIComponent()
        self.reload_scene_button = button_ui_component.ButtonUIComponent()

        # setup object form buttons
        self.save_object_button = button_ui_component.ButtonUIComponent()
        self.cancel_save_button = button_ui_component.ButtonUIComponent()
        self.file_dialog_button = button_ui_component.ButtonUIComponent()
        self.generic_1_sprite_sheet_switch = button_ui_component.ButtonUIComponent(switch=True)
        self.generic_2_sprite_sheet_switch = button_ui_component.ButtonUIComponent(switch=True)
        self.generic_3_sprite_sheet_switch = button_ui_component.ButtonUIComponent(switch=True)
        self.generic_4_sprite_sheet_switch = button_ui_component.ButtonUIComponent(switch=True)

        # setup object form combo boxes
        self.category_combo_box = combo_box_ui_component.ComboBoxUIComponent(200, 25)
        # self.sprite_combo_box = combo_box_ui_component.ComboBoxUIComponent(200, 25)
        self.current_sprite_dir_cb = combo_box_ui_component.ComboBoxUIComponent(200, 25)
        self.generic_sprite_1_dir_cb = combo_box_ui_component.ComboBoxUIComponent(200, 25)
        self.generic_sprite_2_dir_cb = combo_box_ui_component.ComboBoxUIComponent(200, 25)
        self.generic_sprite_3_dir_cb = combo_box_ui_component.ComboBoxUIComponent(200, 25)
        self.generic_sprite_4_dir_cb = combo_box_ui_component.ComboBoxUIComponent(200, 25)
        self.current_sprite_file_cb = combo_box_ui_component.ComboBoxUIComponent(200, 25)
        self.generic_sprite_1_file_cb = combo_box_ui_component.ComboBoxUIComponent(200, 25)
        self.generic_sprite_2_file_cb = combo_box_ui_component.ComboBoxUIComponent(200, 25)
        self.generic_sprite_3_file_cb = combo_box_ui_component.ComboBoxUIComponent(200, 25)
        self.generic_sprite_4_file_cb = combo_box_ui_component.ComboBoxUIComponent(200, 25)

        self.l_button_ui_elements = {}
        self.l_object_component_cb_elements = {}

        self.setup_button_ui()
        self.setup_combo_box_ui()

        # setup attributes ui
        self.attribute_ui = attribute_ui_component.AttributeUIComponent()

        # setup object place
        self.object_placer = object_placer_component.ObjectPlacerComponent()

        # setup a text box
        self.text_box_ui = text_box_ui_component.TextBoxUIComponent()

        self.attribute_ui.l_text_boxes = self.text_box_ui.l_text_boxes
        self.text_box_ui.previous_attribute_components = self.attribute_ui.l_previous_attribute_components

        self.selected_object = None
        self.edit = True
        self.draw_colliders = True

    def update(self, **kwargs):
        d_inputs = kwargs['InputDict']
        game_objects = kwargs['GameObjects']
        e_graphics = kwargs["GraphicsEngine"]

        self.c_object_creator.category_handler(d_inputs)

        self.c_scene.update(GameObjects=game_objects, GraphicsEngine=e_graphics, InputDict=d_inputs,
                            ObjectCreator=self.c_object_creator)

        for key, button in self.l_button_ui_elements.items():
            if button.render:
                button.update(Key=key, InputDict=d_inputs, ALevelEditor=self)

        e_graphics.draw_colliders = self.draw_colliders
        self.attribute_ui.update_selected_object(d_inputs, game_objects)
        self.attribute_ui.update_object_attributes(d_inputs)
        self.attribute_ui.update()
        self.object_container_ui.update_object_container_ui(self.c_object_creator)

        self.object_placer.update(InputDict=d_inputs, GameObjects=game_objects, ALevelEditor=self,
                                  GraphicsEngine=e_graphics)

        self.c_object.update(TextBoxes=self.text_box_ui.l_text_boxes, Buttons=self.l_button_ui_elements,
                             InputDict=d_inputs,
                             ComboBoxes=self.l_object_component_cb_elements)
        self.text_box_ui.get_input(InputDict=d_inputs)

    def setup_button_ui(self):
        # create sprite sheets
        self.play_pause_button.sprite.create_sprite_sheet("./Assets/UI/Buttons/play_pause.png", 4, Vector(32, 32))
        self.add_object_button.sprite.create_sprite_sheet("./Assets/UI/Buttons/add_button_small.png", 2, Vector(32, 32))
        self.remove_object_button.sprite.create_sprite_sheet("./Assets/UI/Buttons/delete_button.png", 2, Vector(32, 32))
        self.back_button.sprite.create_sprite_sheet("./Assets/UI/Buttons/back_button.png", 2, Vector(32, 32))
        self.add_scene_button.sprite.create_sprite_sheet("./Assets/UI/Buttons/add_button_small.png", 2, Vector(32, 32))
        self.save_scene_button.sprite.create_sprite_sheet("./Assets/UI/Buttons/save_button.png", 2, Vector(32, 32))
        self.delete_scene_button.sprite.create_sprite_sheet("./Assets/UI/Buttons/delete_button.png", 2, Vector(32, 32))
        self.reload_scene_button.sprite.create_sprite_sheet("./Assets/UI/Buttons/reload_button.png", 2, Vector(32, 32))
        self.reload_objects_button.sprite.create_sprite_sheet('./Assets/UI/Buttons/reload_button.png',2 , Vector(32,32))
        self.save_object_button.sprite.create_sprite_sheet("./Assets/UI/Buttons/save_object_button.png", 2,
                                                           Vector(128, 64))
        self.cancel_save_button.sprite.create_sprite_sheet("./Assets/UI/Buttons/cancel_object_button.png", 2,
                                                           Vector(32, 32))
        self.file_dialog_button.sprite.create_sprite_sheet("./Assets/UI/Buttons/folder_dialog.png", 2, Vector(32, 32))
        self.collision_button.sprite.create_sprite_sheet("./Assets/UI/Buttons/collision_button.png", 2, Vector(32, 32))
        self.generic_1_sprite_sheet_switch.sprite.create_sprite_sheet("./Assets/UI/Buttons/sprite_sheet_switch.png", 2,
                                                                      Vector(32, 32))
        self.generic_2_sprite_sheet_switch.sprite.create_sprite_sheet("./Assets/UI/Buttons/sprite_sheet_switch.png", 2,
                                                                      Vector(32, 32))
        self.generic_3_sprite_sheet_switch.sprite.create_sprite_sheet("./Assets/UI/Buttons/sprite_sheet_switch.png", 2,
                                                                      Vector(32, 32))
        self.generic_4_sprite_sheet_switch.sprite.create_sprite_sheet("./Assets/UI/Buttons/sprite_sheet_switch.png", 2,
                                                                      Vector(32, 32))
        self.grid_move_switch.sprite.create_sprite_sheet("./Assets/UI/Buttons/grid_mover_switch.png", 2, Vector(32, 32))

        self.save_object_button.render = False
        self.cancel_save_button.render = False
        self.file_dialog_button.render = False
        self.generic_1_sprite_sheet_switch.render = False
        self.generic_2_sprite_sheet_switch.render = False
        self.generic_3_sprite_sheet_switch.render = False
        self.generic_4_sprite_sheet_switch.render = False

        # setup positions
        #self.play_pause_position = Vector(self.screen_width, 25)
        self.play_pause_button.sprite.position = Vector(self.screen_width + 10, 25)
        self.add_object_button.sprite.position = Vector(
            self.screen_width + 10 + self.play_pause_button.sprite.sprite_sheet[-1].get_width() + 5, 25)
        self.remove_object_button.sprite.position = Vector(
            self.add_object_button.sprite.position.x + 5 + self.add_object_button.sprite.sprite_sheet[-1].get_width(),
            25)
        self.collision_button.sprite.position = Vector(
            self.remove_object_button.sprite.position.x + 5 + self.remove_object_button.sprite.sprite_sheet[
                -1].get_width(), 25)
        self.grid_move_switch.sprite.position = Vector(
            self.collision_button.sprite.position.x+5+self.collision_button.sprite.sprite_sheet[-1].get_width(), 25)
        self.reload_objects_button.sprite.position = Vector(
            self.grid_move_switch.sprite.position.x+5+self.grid_move_switch.sprite.sprite_sheet[-1].get_width(), 25)

        self.back_button.sprite.position = Vector(self.screen_width + 10, 170)

        self.save_scene_button.sprite.position = Vector(20, self.screen_height)
        self.add_scene_button.sprite.position = Vector(20, self.screen_height + 32)
        self.delete_scene_button.sprite.position = Vector(20, self.screen_height + 64)
        self.reload_scene_button.sprite.position = Vector(20, self.screen_height + 98)

        self.save_object_button.sprite.position = Vector(self.screen_width * .2 + 50, self.screen_height / 2 + 300)
        self.cancel_save_button.sprite.position = Vector(self.screen_width * .2 + 650, self.screen_height * .15)
        self.file_dialog_button.sprite.position = Vector(self.screen_width * .4 + 200, self.screen_height / 8 + 58)
        self.generic_1_sprite_sheet_switch.sprite.position = Vector(self.screen_width * .2 + 660,
                                                                    self.screen_height * .15 + 105)
        self.generic_2_sprite_sheet_switch.sprite.position = Vector(self.screen_width * .2 + 660,
                                                                    self.screen_height * .15 + 170)
        self.generic_3_sprite_sheet_switch.sprite.position = Vector(self.screen_width * .2 + 660,
                                                                    self.screen_height * .15 + 235)
        self.generic_4_sprite_sheet_switch.sprite.position = Vector(self.screen_width * .2 + 660,
                                                                    self.screen_height * .15 + 300)

        # create sprite sheet rects
        self.play_pause_button.sprite.create_sprite_sheet_rect()
        self.add_object_button.sprite.create_sprite_sheet_rect()
        self.back_button.sprite.create_sprite_sheet_rect()
        self.add_scene_button.sprite.create_sprite_sheet_rect()
        self.save_scene_button.sprite.create_sprite_sheet_rect()
        self.delete_scene_button.sprite.create_sprite_sheet_rect()
        self.reload_scene_button.sprite.create_sprite_sheet_rect()
        self.save_object_button.sprite.create_sprite_sheet_rect()
        self.cancel_save_button.sprite.create_sprite_sheet_rect()
        self.file_dialog_button.sprite.create_sprite_sheet_rect()
        self.remove_object_button.sprite.create_sprite_sheet_rect()
        self.collision_button.sprite.create_sprite_sheet_rect()
        self.generic_1_sprite_sheet_switch.sprite.create_sprite_sheet_rect()
        self.generic_2_sprite_sheet_switch.sprite.create_sprite_sheet_rect()
        self.generic_3_sprite_sheet_switch.sprite.create_sprite_sheet_rect()
        self.generic_4_sprite_sheet_switch.sprite.create_sprite_sheet_rect()
        self.grid_move_switch.sprite.create_sprite_sheet_rect()
        self.reload_objects_button.sprite.create_sprite_sheet_rect()
        # add to ui element
        self.l_button_ui_elements = {'play': self.play_pause_button,
                                     'add': self.add_object_button,
                                     'back': self.back_button,
                                     "add-scene": self.add_scene_button,
                                     "save-scene": self.save_scene_button,
                                     "delete-scene": self.delete_scene_button,
                                     "reload-scene": self.reload_scene_button,
                                     'save-object': self.save_object_button,
                                     'cancel-save': self.cancel_save_button,
                                     'file-dialog': self.file_dialog_button,
                                     'remove-object': self.remove_object_button,
                                     'collision-button': self.collision_button,
                                     'generic_1_sprite_switch': self.generic_1_sprite_sheet_switch,
                                     'generic_2_sprite_switch': self.generic_2_sprite_sheet_switch,
                                     'generic_3_sprite_switch': self.generic_3_sprite_sheet_switch,
                                     'generic_4_sprite_switch': self.generic_4_sprite_sheet_switch,
                                     "grid_move_switch": self.grid_move_switch,
                                     'reload_objects_button': self.reload_objects_button

                                     }

    def setup_combo_box_ui(self):
        self.category_combo_box.set_position(Vector(self.screen_width * .2 + 250, self.screen_height / 8 + 448))
        self.category_combo_box.add_entry("environment_object")
        self.category_combo_box.add_entry("player_object")
        self.category_combo_box.add_entry("item_object")
        self.category_combo_box.add_entry("scene_object")
        self.category_combo_box.add_entry("enemy_object")

        # object creator form directory selection combo boxes
        y_pos = 64
        self.current_sprite_dir_cb.set_position(
            Vector(self.screen_width * .2 + 250, self.screen_height / 8 + y_pos))
        y_pos += 64

        self.generic_sprite_1_dir_cb.set_position(
            Vector(self.screen_width * .2 + 250, self.screen_height / 8 + y_pos))
        y_pos += 64

        self.generic_sprite_2_dir_cb.set_position(
            Vector(self.screen_width * .2 + 250, self.screen_height / 8 + y_pos)
        )
        y_pos += 64

        self.generic_sprite_3_dir_cb.set_position(
            Vector(self.screen_width * .2 + 250, self.screen_height / 8 + y_pos)
        )
        y_pos += 64

        self.generic_sprite_4_dir_cb.set_position(
            Vector(self.screen_width * .2 + 250, self.screen_height / 8 + y_pos)
        )

        # object creator form file selection combo boxes
        y_pos = 64
        self.current_sprite_file_cb.set_position(
            Vector(self.screen_width * .2 + 450, self.screen_height / 8 + y_pos)
        )
        y_pos += 64

        self.generic_sprite_1_file_cb.set_position(
            Vector(self.screen_width * .2 + 450, self.screen_height / 8 + y_pos)
        )
        y_pos += 64

        self.generic_sprite_2_file_cb.set_position(
            Vector(self.screen_width * .2 + 450, self.screen_height / 8 + y_pos)
        )
        y_pos += 64

        self.generic_sprite_3_file_cb.set_position(
            Vector(self.screen_width * .2 + 450, self.screen_height / 8 + y_pos)
        )
        y_pos += 64

        self.generic_sprite_4_file_cb.set_position(
            Vector(self.screen_width * .2 + 450, self.screen_height / 8 + y_pos)
        )
        y_pos += 64

        self.l_object_component_cb_elements = {
            'current_sprite_dir_cb_ocf': self.current_sprite_dir_cb,
            'generic_sprite_1_dir_cb_ocf': self.generic_sprite_1_dir_cb,
            'generic_sprite_2_dir_cb_ocf': self.generic_sprite_2_dir_cb,
            'generic_sprite_3_dir_cb_ocf': self.generic_sprite_3_dir_cb,
            'generic_sprite_4_dir_cb_ocf': self.generic_sprite_4_dir_cb,
            'current_sprite_file_cb_ocf': self.current_sprite_file_cb,
            'generic_sprite_1_file_cb_ocf': self.generic_sprite_1_file_cb,
            'generic_sprite_2_file_cb_ocf': self.generic_sprite_2_file_cb,
            'generic_sprite_3_file_cb_ocf': self.generic_sprite_3_file_cb,
            'generic_sprite_4_file_cb_ocf': self.generic_sprite_4_file_cb,
            'category_combo_box_ocf': self.category_combo_box
        }

