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
        self.tool_bar_position = Vector(self.display_width-5,0)

        self.attr_window_color = (70,70,70)
        self.attr_window_position = Vector(self.display_width+5, 200)
        self.attr_window_size = Vector(365, self.display_height-25)

        self.font = pygame.font.Font(None,36)
        self.font_color = (255,255,255)
        self.font_size = 0.5

        self.l_attribute_components = list()
        self.l_previous_attribute_components = list()
        self.parent_attribute = None
        self.child_attribute = None
    def draw_attributes(self,screen):

        pygame.draw.rect(screen,self.tool_bar_color, (self.tool_bar_position.x,self.tool_bar_position.y,self.tool_bar_size.x,self.tool_bar_size.y))
        pygame.draw.rect(screen,self.attr_window_color, (self.attr_window_position.x,self.attr_window_position.y,self.attr_window_size.x,self.attr_window_size.y))
    
        for attr in self.l_attribute_components:
            attr.update_value()
            screen.blit(attr.attribute_image, (attr.position.x,attr.position.y)) 
            screen.blit(attr.value_image , ((attr.position.x+ attr.x_spacing),attr.position.y ))
        
    def create_attribute_component_list(self,attr_list):
        self.l_attribute_components.clear()
        if pygame.font:
            x_position = self.display_width + 10
            y_position = self.attr_window_position.y + 10
            y_increment = 25
 
            for attr in attr_list:
                    
                self.l_attribute_components.append(AttributeComponent())
                self.l_attribute_components[-1].create_attribute(attr,Vector(x_position,y_position))
                y_position += y_increment

    def update_attributes(self,d_input,c_object_creator):
        mouse_position = pygame.mouse.get_pos()

        for attr in self.l_attribute_components:

            if attr.value_rect.collidepoint(mouse_position):
         
                if d_input['left-click'] and not d_input['left_click_latch']:

                    self.update_attribute_lists(attr,c_object_creator)

                    d_input['left_click_latch'] = True        
            
                elif not d_input['left-click'] and d_input['left_click_latch']:
                
                    d_input['left_click_latch'] = False
       
    def update_attribute_lists(self,attr,c_object_creator):
        if hasattr(attr.attr_data[1], '__dict__'):

            self.l_previous_attribute_components.append(self.l_attribute_components.copy())
            c_object_creator.l_previous_attributes.append(c_object_creator.l_attributes.copy())
            c_object_creator.create_attribute_list(attr.attr_data[1])
            self.create_attribute_component_list(c_object_creator.l_attributes)

    def restore_attribute_components(self,c_object_creator):
        if len(self.l_previous_attribute_components) > 0:
            self.l_attribute_components = self.l_previous_attribute_components.pop()
            c_object_creator.l_attributes = c_object_creator.l_previous_attributes.pop()

class AttributeComponent:

    def __init__(self):

        self.position = Vector(0,0)
        self.attr_data = None
        self.attribute_image = None
        self.value_image = None
        self.value_selected_image = None
        self.value_unselected_image = None
        self.attribute_rect = None
        self.value_rect = None
        self.font = pygame.font.Font(None,18)
        self.font_color = (255,255,255)
        self.select_color = (0,50,225)    
        self.x_spacing = 125
        self.y_increment = 25

    def create_attribute(self,attr, position):
        self.attr_data = attr
        self.position = position
     
        self.attribute_image = self.font.render(str(attr[0]), 1, self.font_color)

        self.value_image = self.font.render(str(attr[1])[:34],1,self.font_color)
    
        self.value_selected_image = self.font.render(str(attr[1])[:34],1,self.select_color)
              
        self.attribute_rect = pygame.Rect(self.position.x, self.position.y,self.attribute_image.get_width(),self.attribute_image.get_height())
      
        self.value_rect = pygame.Rect(self.position.x+self.x_spacing,self.position.y,self.value_image.get_width(),self.value_image.get_height())
      
        self.value_unselected_image = self.value_image


    def update_value(self):
        mouse_position = pygame.mouse.get_pos()

        self.value_image = self.font.render(str(self.attr_data[1])[:34],1,self.font_color)
    
        self.value_selected_image = self.font.render(str(self.attr_data[1])[:34],1,self.select_color)
        
        self.value_unselected_image = self.value_image

        if self.value_rect.collidepoint(mouse_position):

            self.value_image = self.value_selected_image
            
        else:
            self.value_image = self.value_unselected_image
         
          