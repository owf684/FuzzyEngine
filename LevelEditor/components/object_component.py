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
        self.category_combo_box.set_position(Vector(self.display_width*.2 + 250,self.display_height/8 + 448))
        self.category_combo_box.add_entry("environment_object")
        self.category_combo_box.add_entry("game_object")
        self.category_combo_box.add_entry("item_object")
        self.category_combo_box.add_entry("scene_object")
        self.sprite_combo_box = combo_box_ui_component.ComboBoxUIComponent(200,25)
        self.sprite_combo_box.set_position(Vector(self.display_width*.2 + 250,self.display_height/8 + 64))
        self.skip_update = False
        self.skip_update_2 = False
        self.current_cb = 0
        self.current_cb_2 = 0
        self.generic_1_sprite_is_sheet = False
        self.generic_2_sprite_is_sheet = False
        self.generic_3_sprite_is_sheet = False
        self.generic_4_sprite_is_sheet = False     

        self.sprite_dir_combo_box = list()
        y_pos = 64
        self.sprite_dir_cb_index = list()
        for i in range(5):
            self.sprite_dir_combo_box.append(combo_box_ui_component.ComboBoxUIComponent(200,25))
            self.sprite_dir_combo_box[-1].set_position(Vector(self.display_width*.2 + 250,self.display_height/8 + y_pos))
            self.sprite_dir_cb_index.append(self.sprite_dir_combo_box[-1].selected_index)

            y_pos += 64

        self.current_sprite_cb = list()
        self.sprite_cb = list()

        self.d_inputs = None
        self.class_name_value = ''

    def update(self,**kwargs):
        self.l_text_boxes = kwargs['TextBoxes']
        self.l_button_ui_elements = kwargs['Buttons']
        self.d_inputs = kwargs['InputDict']
    def draw_object_prompt(self,screen):

        if self.trigger_object_prompt:
            self.category_combo_box.update(InputDict=self.d_inputs)

            i = len(self.sprite_dir_combo_box)-1
            for cb in reversed(self.sprite_dir_combo_box):
                
                if not self.skip_update:
                    cb.update(InputDict=self.d_inputs)
                    self.sprite_dir_cb_index[i] = cb.selected_index
                    if cb.show_entries:
                        self.skip_update = True
                        self.current_cb = self.sprite_dir_combo_box.index(cb)

                if self.skip_update and self.sprite_dir_combo_box.index(cb) == self.current_cb:
                    cb.update(InputDict=self.d_inputs)
                    self.sprite_dir_cb_index[i] = cb.selected_index
                    self.skip_update = cb.show_entries
                i -= 1
          
            i = len(self.sprite_dir_combo_box)-1
            for cb in reversed(self.sprite_cb):
                if not self.skip_update_2:
                    cb[self.sprite_dir_cb_index[i]].update(InputDict=self.d_inputs)

                    if cb[self.sprite_dir_cb_index[i]].show_entries:
                        self.skip_update_2 = True
                        self.current_cb_2 = self.sprite_cb.index(cb)
                if self.skip_update_2 and self.sprite_cb.index(cb) == self.current_cb_2:
                    cb[self.sprite_dir_cb_index[i]].update(InputDict=self.d_inputs)
                    self.skip_update_2 = cb[self.sprite_dir_cb_index[i]].show_entries

                i -= 1
            pygame.draw.rect(screen,(45,45,45),(self.display_width*.2,self.display_height/8,700,self.display_height+50))
            
            current_sprite = self.font.render("Current Sprite:", 1, self.font_color)
            screen.blit(current_sprite,(self.display_width*.2+50,self.display_height/8 + 64))

            generic_sprite_1 = self.font.render("Generic Sprite 1:", 1, self.font_color)
            screen.blit(generic_sprite_1,(self.display_width*.2+50,self.display_height/8 + 128))

            generic_sprite_2 = self.font.render("Generic Sprite 2:", 1, self.font_color)
            screen.blit(generic_sprite_2,(self.display_width*.2+50,self.display_height/8 + 192))

            generic_sprite_3 = self.font.render("Generic Sprite 3:", 1, self.font_color)
            screen.blit(generic_sprite_3,(self.display_width*.2+50,self.display_height/8 + 256))

            generic_sprite_4 = self.font.render("Generic Sprite 4:", 1, self.font_color)
            screen.blit(generic_sprite_4,(self.display_width*.2+50,self.display_height/8 + 320))

            object_file = self.font.render("Object Class:", 1, self.font_color)
            screen.blit(object_file,(self.display_width*.2+50,self.display_height/8 + 384))

            object_class = self.font.render("Object Category:", 1, self.font_color)
            screen.blit(object_class,(self.display_width*.2+50,self.display_height/8 + 448))
            
            self.category_combo_box.draw_combo_box(screen)

            for cb in reversed(self.sprite_dir_combo_box):
                cb.draw_combo_box(screen)
            i = len(self.sprite_dir_combo_box)-1
            for cb in reversed(self.sprite_cb):
                cb[self.sprite_dir_cb_index[i]].draw_combo_box(screen)
                i -= 1
            self.l_button_ui_elements['save-object'].render = True
            self.l_button_ui_elements['cancel-save'].render = True
            self.l_button_ui_elements['generic_1_sprite_switch'].render = True
            self.l_button_ui_elements['generic_2_sprite_switch'].render = True
            self.l_button_ui_elements['generic_3_sprite_switch'].render = True
            self.l_button_ui_elements['generic_4_sprite_switch'].render = True

            if  self.add_text_boxes and self.sprite_dir_combo_box[-1].show_entries and len(self.sprite_dir_combo_box[-1].entries) >=2:
                self.class_name_value = self.l_text_boxes[-1].userInput
                self.l_text_boxes.pop()
                self.add_text_boxes = False
       

            if not self.add_text_boxes and not self.sprite_dir_combo_box[-1].show_entries:

                textBox2 = text_box_ui_component.TextBox(200,25,Vector(self.display_width*.2 + 250,self.display_height/8 + 384))
                textBox2.userInput = self.class_name_value
                self.l_text_boxes.append(textBox2)                
                self.add_text_boxes = True

    def find_sprites(self):
        for cb in self.sprite_dir_combo_box:
            cb.reset()
        self.sprite_cb.clear()
        y_pos = 64

        for cb in self.sprite_dir_combo_box:
            new_cb = list()
            for root, dirs, files in os.walk("./GameData/Assets/"):
                if len(root[18:]) > 0:
                    cb.add_entry(root[18:])

                    new_cb.append(combo_box_ui_component.ComboBoxUIComponent(200,25))
                    new_cb[-1].set_position(Vector(self.display_width*.2 + 450,self.display_height/8 + y_pos))
                    new_cb[-1].add_entry('None')
                for pngs in files:
                    if ".png" in pngs:
                        new_cb[-1].add_entry(pngs,directory=root[18:])
        
                if len(new_cb) > 0 and len(new_cb[-1].entries) == 1:
                    new_cb.pop()
                    cb.y_gap -= cb.height
                    cb.entries.pop()
            
            self.sprite_cb.append(new_cb)
            y_pos += 64
 
    def cancel_prompt(self):
        self.add_text_boxes = False
        self.trigger_object_prompt = False
        self.l_button_ui_elements['save-object'].render = False
        self.l_button_ui_elements['cancel-save'].render = False
        self.l_button_ui_elements['file-dialog'].render = False
        self.l_button_ui_elements['generic_1_sprite_switch'].render = False
        self.l_button_ui_elements['generic_2_sprite_switch'].render = False
        self.l_button_ui_elements['generic_3_sprite_switch'].render = False
        self.l_button_ui_elements['generic_4_sprite_switch'].render = False
        self.class_name_value = ''
        self.current_sprite_cb.clear()

        self.l_text_boxes.clear()


    def save_object(self):
        current_sprite = self.sprite_cb[0][self.sprite_dir_cb_index[0]].get_directory() + "/" + self.sprite_cb[0][self.sprite_dir_cb_index[0]].get_value()
        generic_sprite_1 = self.sprite_cb[1][self.sprite_dir_cb_index[1]].get_directory() + "/" + self.sprite_cb[1][self.sprite_dir_cb_index[1]].get_value()
        generic_sprite_2 = self.sprite_cb[2][self.sprite_dir_cb_index[2]].get_directory() + "/" + self.sprite_cb[2][self.sprite_dir_cb_index[2]].get_value()
        generic_sprite_3 = self.sprite_cb[3][self.sprite_dir_cb_index[3]].get_directory() + "/" + self.sprite_cb[3][self.sprite_dir_cb_index[3]].get_value()
        generic_sprite_4 = self.sprite_cb[4][self.sprite_dir_cb_index[4]].get_directory() + "/" + self.sprite_cb[4][self.sprite_dir_cb_index[4]].get_value()
       
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
        file_template = object_template.get_file_template()
        file_template['parent_object'] = "import " + object_category
        file_template['class_define'] = 'class ' + object_class + '(' + object_category + "." + object_template.object_categories[object_category] + "):"
        
        if 'None' not in current_sprite:
            file_template['current_sprite'] = "self.current_sprite.create_sprite('./GameData/Assets/"+current_sprite+"')" 
        else: file_template.pop('current_sprite')

        if 'None' not in generic_sprite_1:
            if self.generic_1_sprite_is_sheet:
                file_template['generic_sprite_1'] = ("self.generic_sprite_1.create_sprite_sheet('./GameData/Assets/"+generic_sprite_1,1,Vector(32,32))
      
            else:
                file_template['generic_sprite_1'] = "self.generic_sprite_1.create_sprite('./GameData/Assets/"+generic_sprite_1+"')"  
                file_template.pop('generic_sprite_1_position')
                file_template.pop("generic_sprite_1_rect")            
        else: 
            file_template.pop("generic_sprite_1")
            file_template.pop('generic_sprite_1_position')
            file_template.pop("generic_sprite_1_rect")
        if 'None' not in generic_sprite_2:
            if self.generic_2_sprite_is_sheet:
                file_template['generic_sprite_2'] = ("self.generic_sprite_2.create_sprite_sheet('./GameData/Assets/"+generic_sprite_2,1,Vector(32,32))

            else:
                file_template['generic_sprite_2'] = "self.generic_sprite_2.create_sprite('./GameData/Assets/"+generic_sprite_2+"')" 
                file_template.pop('generic_sprite_2_position')
                file_template.pop("generic_sprite_2_rect") 
        else: 
            file_template.pop("generic_sprite_2")
            file_template.pop('generic_sprite_2_position')
            file_template.pop("generic_sprite_2_rect")
        if 'None' not in generic_sprite_3:
            if self.generic_3_sprite_is_sheet:
                file_template['generic_sprite_3'] = ("self.generic_sprite_3.create_sprite_sheet('./GameData/Assets/"+generic_sprite_3,1,Vector(32,32))

            else:
                file_template['generic_sprite_3'] = "self.generic_sprite_3.create_sprite('./GameData/Assets/"+generic_sprite_3+"')"     
                file_template.pop('generic_sprite_3_position')
                file_template.pop("generic_sprite_3_rect")
        else: 
            file_template.pop("generic_sprite_3")
            file_template.pop('generic_sprite_3_position')
            file_template.pop("generic_sprite_3_rect")

        if 'None' not in generic_sprite_4:
            if self.generic_4_sprite_is_sheet:
                file_template['generic_sprite_4'] = ("self.generic_sprite_4.create_sprite_sheet('./GameData/Assets/"+generic_sprite_4,1,Vector(32,32))

            else:
                file_template['generic_sprite_4'] = "self.generic_sprite_4.create_sprite('./GameData/Assets/"+generic_sprite_4+"')" 
                file_template.pop('generic_sprite_4_position')
                file_template.pop("generic_sprite_4_rect")

        else: 
            file_template.pop("generic_sprite_4")
            file_template.pop('generic_sprite_4_position')
            file_template.pop("generic_sprite_4_rect")

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