import pygame
import sys
sys.path.append("./Objects/components")
import text_box_ui_component
from vector import Vector
class ObjectComponent:

    def __init__(self):
        self.trigger_object_prompt = False
        self.display_info = pygame.display.Info()
        self.display_width = int(self.display_info.current_w*.8)
        self.display_height = int(self.display_info.current_h*.8)
        self.l_text_boxes = list()
        self.add_text_boxes = False
        self.font = pygame.font.Font(None,24)
        self.font_color = (255,255,255)
        self.l_button_ui_elements = list()

    def update(self,**kwargs):
        self.l_text_boxes = kwargs['TextBoxes']
        self.l_button_ui_elements = kwargs['Buttons']
    def draw_object_prompt(self,screen):

        if self.trigger_object_prompt:
            pygame.draw.rect(screen,(70,70,70),(self.display_width*.4,self.display_height/8,500,self.display_height))
            
            object_directory = self.font.render("Object Directory:", 1, self.font_color)
            screen.blit(object_directory,(self.display_width*.4+50,self.display_height/8 + 64))
        
            object_file = self.font.render("Object File:", 1, self.font_color)
            screen.blit(object_file,(self.display_width*.4+50,self.display_height/8 + 128))

            object_class = self.font.render("Object Class:", 1, self.font_color)
            screen.blit(object_class,(self.display_width*.4+50,self.display_height/8 + 192))

            object_category = self.font.render("Object Category:", 1, self.font_color)
            screen.blit(object_category,(self.display_width*.4+50,self.display_height/8 + 256))

            self.l_button_ui_elements['save-object'].render = True
            self.l_button_ui_elements['cancel-save'].render = True
            if not self.add_text_boxes:

                textBox1 = text_box_ui_component.TextBox(200,25,Vector(self.display_width*.4 + 250,self.display_height/8 + 64))
                self.l_text_boxes.append(textBox1)

                textBox2 = text_box_ui_component.TextBox(200,25,Vector(self.display_width*.4 + 250,self.display_height/8 + 128))
                self.l_text_boxes.append(textBox2)

                textBox3 = text_box_ui_component.TextBox(200,25,Vector(self.display_width*.4 + 250,self.display_height/8 + 192))
                self.l_text_boxes.append(textBox3)

                textBox4 = text_box_ui_component.TextBox(200,25,Vector(self.display_width*.4 + 250,self.display_height/8 + 256))
                self.l_text_boxes.append(textBox4)      

                self.add_text_boxes = True

    def cancel_prompt(self):
        self.add_text_boxes = False
        self.trigger_object_prompt = False
        self.l_button_ui_elements['save-object'].render = False
        self.l_button_ui_elements['cancel-save'].render = False
        self.l_text_boxes.clear()


    def save_object(self):
        for boxes in self.l_text_boxes:
            print(boxes.userInput)