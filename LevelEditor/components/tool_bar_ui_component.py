import sys
import pygame
sys.path.append("./Objects/components")
from vector import Vector

class ToolBarUIComponent:

    def __init__(self): 
        self.display_info = pygame.display.Info()
        self.display_width = int(self.display_info.current_w*.8)
        self.display_height = int(self.display_info.current_h*.8)
        
        self.tool_bar_color = (30,30,30)
        self.tool_bar_size = Vector(400,self.display_height + 200) 
        self.tool_bar_position = Vector(self.display_width,0)

    
    def draw_toolbar(self,screen):

        pygame.draw.rect(screen,self.tool_bar_color, (self.tool_bar_position.x,self.tool_bar_position.y,self.tool_bar_size.x,self.tool_bar_size.y))
    
        
