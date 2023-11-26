import sys
import pygame
sys.path.append("./Objects/components")
import sprite_component
from vector import Vector

class ButtonUIComponent:

    def __init__(self, switch=False):
        # get display info
        self.display_info = pygame.display.Info()
        self.screen_width = int(self.display_info.current_w*.8)
        self.screen_height = int(self.display_info.current_h*.8)

        self.sprite = sprite_component.SpriteComponent()
        self.button_state = ButtonState(0,1)
        self.button_signal = ButtonSignal()
        self.toggled = False
        self.switch = switch
        self.render = True

    def set_animation_state(self,d_inputs):

        mouse_position = pygame.mouse.get_pos()

        # default button behavior
        if not self.switch:

            if self.sprite.rect.collidepoint(mouse_position):
                self.sprite.animation_state = self.button_state.state_1
            else:
                self.sprite.animation_state = self.button_state.state_2

            if self.sprite.rect.collidepoint(mouse_position):
                 if d_inputs['left-click'] and not d_inputs['left_click_latch']:
                    d_inputs['left_click_latch'] = True
                    self.toggled = True

        # switch button behavior 
        elif self.switch:
            if self.sprite.rect.collidepoint(mouse_position):

                if d_inputs['left-click'] and not d_inputs['left_click_latch'] and not self.toggled:
                    d_inputs['left_click_latch'] = True
                    self.toggled = True
                    self.sprite.animation_state = self.button_state.state_2
                if d_inputs['left-click'] and not d_inputs['left_click_latch'] and self.toggled:
                    d_inputs['left_click_latch'] = True
                    self.toggled = False
                    self.sprite.animation_state = self.button_state.state_1

        # update latch
        if not d_inputs['left-click'] and d_inputs['left_click_latch']:
            d_inputs['left_click_latch'] = False                

    def draw_button(self,screen):
        if len(self.sprite.sprite_sheet)>0:
                if self.sprite.sprite_sheet[self.sprite.animation_state] is not None:
                    screen.blit(self.sprite.sprite_sheet[self.sprite.animation_state],(self.sprite.position.x,self.sprite.position.y))

    def update(self,**kwargs):
        d_inputs = kwargs['InputDict']
        key = kwargs['Key']        
        self.set_animation_state(d_inputs)
        match key:
            case 'play':
                if self.toggled:
                    if (self.button_state.state_1 == 0): self.button_state = ButtonState(2,3)
                    elif (self.button_state.state_1 == 2): self.button_state = ButtonState(0,1)
                    self.toggled = False
                    self.button_signal.send(**kwargs)
            case 'add':
                if self.toggled:
                    self.toggled = False
                    self.button_signal.send(**kwargs)   
            case 'back':
                if self.toggled:
                    self.toggled = False 
                    self.button_signal.send(**kwargs)
            case "add-scene":
                if self.toggled:
                    self.toggled = False
                    self.button_signal.send(**kwargs)
            case 'save-scene':
                if self.toggled:
                    self.toggled = False
                    self.button_signal.send(**kwargs)
            case 'delete-scene':
                if self.toggled:
                    self.toggled = False
                    self.button_signal.send(**kwargs)
            case 'reload-scene':
                if self.toggled:
                    self.toggled = False
                    self.button_signal.send(**kwargs)
            case 'save-object':
                if self.toggled:
                    self.toggled = False
                    self.button_signal.send(**kwargs)
            case 'cancel-save':
                if self.toggled:
                    self.toggled = False
                    self.button_signal.send(**kwargs)
            case 'file-dialog':
                if self.toggled:
                    self.toggled = False
                    self.button_signal.send(**kwargs)
            case 'remove-object':
                if self.toggled:
                    self.toggled = False
                    self.button_signal.send(**kwargs)
            case 'collision-button':
                if self.toggled:
                    self.toggled = False
                    self.button_signal.send(**kwargs)

            case 'generic_1_sprite_switch':
                self.button_signal.send(**kwargs)
            case 'generic_2_sprite_switch':
                self.button_signal.send(**kwargs)
            case 'generic_3_sprite_switch':
                self.button_signal.send(**kwargs)
            case 'generic_4_sprite_switch':
                self.button_signal.send(**kwargs)
            case _:
                None
            
class ButtonState:
    
    def __init__(self,state_1,state_2):
        self.state_1 = state_1
        self.state_2 = state_2 


class ButtonSignal:

    def send(self,**kwargs):
        key = kwargs['Key']
        level_editor = kwargs['ALevelEditor']
       
        match key:
            case 'play':
                level_editor.edit = not level_editor.edit

            case 'back':
                level_editor.attribute_ui.restore_attribute_components()
            
            case 'add':
                level_editor.c_object.find_sprites()
                level_editor.c_object.trigger_object_prompt = True
                level_editor.object_placer.place_enabled = False
            
            case 'add-scene':
                level_editor.c_scene.add_scene()

            case 'save-scene':
                level_editor.c_scene.b_save_scene = True

            case 'delete-scene':
                level_editor.c_scene.delete_scene()
            case 'reload-scene':
                level_editor.c_scene.load_scene()
            case 'save-object':
                level_editor.c_object.save_object()
                level_editor.object_placer.place_enabled = True
                level_editor.c_object_creator.reset()
                level_editor.c_object_creator.create_json_list()
                level_editor.c_object_creator.create_objects_dict()
                level_editor.c_object_creator.organize_objects()
                level_editor.object_container_ui.init_ui(level_editor.c_object_creator)
            case 'cancel-save':
                level_editor.c_object.cancel_prompt()
                level_editor.object_placer.place_enabled = True
            case 'file-dialog':
                level_editor.c_object.get_directory()
            case 'remove-object':
                if level_editor.c_object_creator.destroy_selected_object():
                    level_editor.c_object_creator.reset()
                    level_editor.c_object_creator.create_json_list()
                    level_editor.c_object_creator.create_objects_dict()
                    level_editor.c_object_creator.organize_objects()
                    level_editor.object_container_ui.init_ui(level_editor.c_object_creator)
            case 'collision-button':
                level_editor.draw_colliders = not level_editor.draw_colliders

            case 'generic_1_sprite_switch':
                level_editor.c_object.generic_1_sprite_is_sheet = level_editor.generic_1_sprite_sheet_switch.toggled

            case 'generic_2_sprite_switch':
                level_editor.c_object.generic_2_sprite_is_sheet = level_editor.generic_2_sprite_sheet_switch.toggled

            case 'generic_3_sprite_switch':
                level_editor.c_object.generic_3_sprite_is_sheet = level_editor.generic_3_sprite_sheet_switch.toggled
                                                        

            case 'generic_4_sprite_switch':
                level_editor.c_object.generic_4_sprite_is_sheet = level_editor.generic_4_sprite_sheet_switch.toggled
                                                        
            case _:
                None

       

