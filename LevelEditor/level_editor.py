import sys
import pygame
sys.path.append("./LevelEditor/components")
sys.path.append("./Objects/components")
import object_creator_component
import object_editor_ui_component
import button_ui_component
import grid_component
import tool_bar_ui_component
from vector import Vector
class LevelEditor:

    def __init__(self):
        # get display info
        self.display_info = pygame.display.Info()
        self.screen_width = int(self.display_info.current_w*.8)
        self.screen_height = int(self.display_info.current_h*.8)

        # setup object creator
        self.c_object_creator = object_creator_component.ObjectCreatorComponent()
        self.c_object_creator.s_directory_path ='./GameData/jsons'
        self.c_object_creator.create_json_list()
        self.c_object_creator.create_objects_dict()
        self.c_object_creator.organize_objects()

        # setup grid component
        self.grid = grid_component.GridComponent()

        # setup tool bar
        self.tool_bar = tool_bar_ui_component.ToolBarUIComponent()
        
        # setup editor ui
        self.object_editor_ui = object_editor_ui_component.ObjectEditorUIComponent()
        self.object_editor_ui.init_ui(self.c_object_creator)

        # setup button ui
        self.play_pause_button = button_ui_component.ButtonUIComponent()
        self.back_button = button_ui_component.ButtonUIComponent()
        self.add_object_button = button_ui_component.ButtonUIComponent()
        self.l_button_ui_elements = {}

        self.setup_button_ui()
 
        self.selected_object = None
        self.edit = True

    def update(self,**kwargs):
        d_inputs=kwargs['InputDict']
        game_objects = kwargs['GameObjects']

        self.update_objects(d_inputs)
        self.update_buttons(d_inputs)
        self.update_attributes(d_inputs,game_objects)
        self.update_ui(d_inputs)
        self.place_object(d_inputs,game_objects)

        return self.object_editor_ui.l_object_editor_ui_elements, self.l_button_ui_elements
    
    def update_objects(self,d_inputs):
        self.c_object_creator.category_handler(d_inputs)

    def update_buttons(self,d_inputs):
        for key , button in self.l_button_ui_elements.items():
            button.update(d_inputs)
            match key:
                case 'play':
                    if button.toggled:
                        if (button.button_state.state_1 == 0): button.button_state = button_ui_component.ButtonState(2,3)
                        elif (button.button_state.state_1 == 2): button.button_state = button_ui_component.ButtonState(0,1)
                        self.edit = not self.edit
                        button.toggled = False
                case 'add':
                    if button.toggled:
                        button.toggled = False
                case 'back':
                    if button.toggled:
                        self.tool_bar.restore_attribute_components(self.c_object_creator)
                        button.toggled = False
                case _:
                    None
    def update_attributes(self,d_inputs,game_objects):
        mouse_position = pygame.mouse.get_pos()

        for objects in game_objects:
            if objects.current_sprite.rect.collidepoint(mouse_position):
                if d_inputs['left-click'] and not d_inputs['left_click_latch']:
                    d_inputs['left_click_latch'] = True
                    
                    self.selected_object = objects
                    self.c_object_creator.create_attribute_list(objects)
                    self.tool_bar.create_attribute_component_list(self.c_object_creator.l_attributes)                    

                elif not d_inputs['left-click'] and d_inputs['left_click_latch']:
                    d_inputs["left_click_latch"] = False

    def update_ui(self,d_inputs):
 
        self.object_editor_ui.update_object_container_ui(self.c_object_creator)
        self.tool_bar.update_attributes(d_inputs,self.c_object_creator)


    def setup_button_ui(self):
        # create sprite sheets
        self.play_pause_button.sprite.create_sprite_sheet("./Assets/UI/Buttons/play_pause.png",4,Vector(64,64))
        self.add_object_button.sprite.create_sprite_sheet("./Assets/UI/Buttons/add_button.png",2,Vector(64,64))
        self.back_button.sprite.create_sprite_sheet("./Assets/UI/Buttons/back_button.png",2,Vector(32,32))
   
        # setup positions
        self.play_pause_position = Vector(self.screen_width+100,25)
        self.play_pause_button.sprite.position.x = self.screen_width + 100
        self.play_pause_button.sprite.position.y = 25
        self.add_object_button.sprite.position.x = self.screen_width + 175
        self.add_object_button.sprite.position.y = 25
        self.back_button.sprite.position.x = self.screen_width+10
        self.back_button.sprite.position.y = 170

        # create sprite sheet rects
        self.play_pause_button.sprite.create_sprite_sheet_rect()
        self.add_object_button.sprite.create_sprite_sheet_rect()
        self.back_button.sprite.create_sprite_sheet_rect()

        # add to ui element
        self.l_button_ui_elements = {'play':    self.play_pause_button,
                                     'add' :    self.add_object_button,
                                     'back':    self.back_button}
    
    def place_object(self,d_inputs,game_objects):
        mouse_position = pygame.mouse.get_pos()

        if self.edit and d_inputs['left-click'] and not d_inputs['left_click_latch']:
            d_inputs['left_click_latch'] = True

            module = self.c_object_creator.get_selected_object()[1]
            obj = self.c_object_creator.d_modules[module].create_object()
            if 0 < mouse_position[0] < self.grid.screen_width and \
                0 < mouse_position[1] < self.grid.screen_height:

                # check if object is already there is there?
                if self.object_exists(mouse_position,game_objects):
                    self.update_position(mouse_position,obj,game_objects)


        elif not d_inputs['left-click'] and d_inputs["left_click_latch"]:
            d_inputs["left_click_latch"] = True

    def object_exists(self,mouse_position,game_objects):
        for objects in game_objects:
            if objects.current_sprite.rect.collidepoint(mouse_position):
                return False
        return True
    def update_position(self,mouse_position,obj,game_objects):
        snap_position = [0,0]
       
        if mouse_position[0] < self.grid.grid_size:
            snap_position[0] = 0
        else:
            snap_position[0] = int((mouse_position[0] - abs(self.grid.scroll_delta))/self.grid.grid_size)*self.grid.grid_size + abs(self.grid.scroll_delta)                
            snap_position[1] = int(mouse_position[1]/self.grid.grid_size)*self.grid.grid_size
            game_objects.append(obj)
            game_objects[-1].physics.initial_position.x = snap_position[0]
            game_objects[-1].physics.initial_position.y = snap_position[1]
            game_objects[-1].physics.position = game_objects[-1].physics.initial_position()
            game_objects[-1].current_sprite.position.x = snap_position[0]
            game_objects[-1].current_sprite.position.y = snap_position[1]
        