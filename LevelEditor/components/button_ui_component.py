import sys
import pygame
sys.path.append("./Objects/components")
import sprite_component
from vector import Vector

class ButtonUIComponent:

    def __init__(self):
        # get display info
        self.display_info = pygame.display.Info()
        self.screen_width = int(self.display_info.current_w*.8)
        self.screen_height = int(self.display_info.current_h*.8)

        self.sprite = sprite_component.SpriteComponent()
        self.button_state = ButtonState(0,1)
        self.toggled = False

    def update(self,d_inputs):

        mouse_position = pygame.mouse.get_pos()
        # update animation if mouse hovers over button
        if self.sprite.rect.collidepoint(mouse_position):
            self.sprite.animation_state = self.button_state.state_1
        else:
            self.sprite.animation_state = self.button_state.state_2

        if self.sprite.rect.collidepoint(mouse_position):
             if d_inputs['left-click'] and not d_inputs['left_click_latch']:
                d_inputs['left_click_latch'] = True
                self.toggled = True                    
        if not d_inputs['left-click'] and d_inputs['left_click_latch']:
            d_inputs['left_click_latch'] = False

class ButtonState:
    
    def __init__(self,state_1,state_2):
        self.state_1 = state_1
        self.state_2 = state_2  

       

