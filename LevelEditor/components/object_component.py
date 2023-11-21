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
        self.directory_path = None
        self.category_combo_box = combo_box_ui_component.ComboBoxUIComponent(200,25)
        self.category_combo_box.set_position(Vector(self.display_width*.4 + 250,self.display_height/8 + 192))
        self.category_combo_box.add_entry("environment_object")
        self.category_combo_box.add_entry("game_object")
        self.category_combo_box.add_entry("item_object")
        self.category_combo_box.add_entry("scene_object")
        self.sprite_combo_box = combo_box_ui_component.ComboBoxUIComponent(200,25)
        self.sprite_combo_box.set_position(Vector(self.display_width*.4 + 250,self.display_height/8 + 64))
        self.sprite_dir_combo_box = combo_box_ui_component.ComboBoxUIComponent(200,25)
        self.sprite_dir_combo_box.set_position(Vector(self.display_width*.4 + 50,self.display_height/8 + 64))
     
        self.d_inputs = None
        self.class_name_value = ''

    def update(self,**kwargs):
        self.l_text_boxes = kwargs['TextBoxes']
        self.l_button_ui_elements = kwargs['Buttons']
        self.d_inputs = kwargs['InputDict']
    def draw_object_prompt(self,screen):

        if self.trigger_object_prompt:
            if not self.sprite_combo_box.show_entries and not self.sprite_dir_combo_box.show_entries:
                self.category_combo_box.update(InputDict=self.d_inputs)
            self.sprite_combo_box.update(InputDict=self.d_inputs)
            self.sprite_dir_combo_box.update(InputDict=self.d_inputs)

            pygame.draw.rect(screen,(70,70,70),(self.display_width*.4,self.display_height/8,500,self.display_height))
            
            object_directory = self.font.render("Sprite Directory:", 1, self.font_color)
            screen.blit(object_directory,(self.display_width*.4+50,self.display_height/8 + 64 -self.sprite_dir_combo_box.height))
        
            object_file = self.font.render("Object Class:", 1, self.font_color)
            screen.blit(object_file,(self.display_width*.4+50,self.display_height/8 + 128))

            object_class = self.font.render("Object Category:", 1, self.font_color)
            screen.blit(object_class,(self.display_width*.4+50,self.display_height/8 + 192))
            
            self.category_combo_box.draw_combo_box(screen)
            self.sprite_combo_box.draw_combo_box(screen)
            self.sprite_dir_combo_box.draw_combo_box(screen)

            self.l_button_ui_elements['save-object'].render = True
            self.l_button_ui_elements['cancel-save'].render = True

            if (self.sprite_combo_box.show_entries )and self.add_text_boxes:
                self.class_name_value = self.l_text_boxes[-1].userInput
                self.l_text_boxes.pop()
                self.add_text_boxes = False
                        
            if not self.add_text_boxes and not self.sprite_combo_box.show_entries:


                textBox2 = text_box_ui_component.TextBox(200,25,Vector(self.display_width*.4 + 250,self.display_height/8 + 128))
                textBox2.userInput = self.class_name_value
                self.l_text_boxes.append(textBox2)
                   
                self.add_text_boxes = True

    def find_sprites(self):
        self.sprite_combo_box.reset()
        self.sprite_dir_combo_box.reset()
        for root, dirs, files in os.walk("./GameData/Assets/"):
            if len(root[18:]) > 0:
                self.sprite_dir_combo_box.add_entry(root[18:])
                
            for pngs in files:
                if ".png" in pngs:
                    self.sprite_combo_box.add_entry(pngs,directory=root[18:])
        
                    
    def cancel_prompt(self):
        self.add_text_boxes = False
        self.trigger_object_prompt = False
        self.l_button_ui_elements['save-object'].render = False
        self.l_button_ui_elements['cancel-save'].render = False
        self.l_button_ui_elements['file-dialog'].render = False
        self.class_name_value = ''
        self.l_text_boxes.clear()


    def save_object(self):
        sprite_dir = self.sprite_combo_box.get_directory() + "/" + self.sprite_combo_box.get_value()
        object_class =self.l_text_boxes[0].userInput
        object_category = self.category_combo_box.get_value()

        file_directory = './GameData/'+object_template.object_categories[object_category] +'s'
        class_name = ''
        file_name =''
        makeUpper = True
        uppersFound = 0

        '''Convert class_name => ClassName'''
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
            '''convert ClassName => class_name'''
            for characters in object_class:
                
                if characters == characters.upper():
                    if uppersFound >0:
                        file_name += '_'
                    file_name += characters.lower()
                    uppersFound += 1
                else:
                    file_name += characters
        file_name += '.py'
                
        # update file template
        file_template = object_template.file_template
        file_template['parent_object'] = "import " + object_category
        file_template['class_define'] = 'class ' + object_class + '(' + object_category + "." + object_template.object_categories[object_category] + "):"
        file_template['current_sprite'] = "self.current_sprite.create_sprite('./GameData/Assets/"+sprite_dir+"')" 
        file_template['object_json_file'] = "self.save_state.object_json_file='./GameData/jsons/" + file_name.rstrip('.py')+".json'"
        file_template['object_return'] = "return " + object_class + "()"
      
        object_template.create_object_file(file_directory, file_name,file_template)
      
        # create object json 
        object_json = {
            "object_directory": file_directory,
            "object_file": file_name,
            "object_class": object_class,
            "object_category": object_category
        }
        with open("./GameData/jsons/" + file_name.rstrip('.py')+".json",'w') as json_file:
            json.dump(object_json,json_file)
      
        self.cancel_prompt()

    def get_directory(self):
        None