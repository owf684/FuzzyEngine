import pygame
import sys

class EditorUIComponent:

    def __init__(self):
        self.ui_elements = list()
        display_info = pygame.display.Info()
        self.screen_width = display_info.current_w/1.2
        self.screen_height = display_info.current_h/1.2
        self.object_container_path = './GameData/Assets/UI/Containers/ObjectContainer.png'
        self.object_container_selected_path = './GameData/Assets/UI/Containers/ObjectContainer_selected.png'



    def init_ui(self,c_object_creator):
        self.ui_elements.clear()
        y_position =32
        print(c_object_creator.l_categories)
        x_position = (self.screen_width/2) - len(c_object_creator.l_categories[c_object_creator.i_category])*64/3
        for objects in c_object_creator.l_categories[c_object_creator.i_category]:
            objects[0].physics.pause = True
            objects[0].generic_sprite_1.create_sprite(self.object_container_path)
            objects[0].generic_sprite_1.position.x = x_position
            objects[0].generic_sprite_1.position.y = y_position


            image_width = objects[0].current_sprite.image.get_width()
            image_height = objects[0].current_sprite.image.get_height()
            image = objects[0].current_sprite.image
            x_scale_facotr = image_width/36
            y_scale_factor = image_height/36
            scale_factor = max(x_scale_facotr,y_scale_factor)
            objects[0].current_sprite.image = pygame.transform.scale(image , (image_width/scale_factor, image_height/scale_factor) )

            objects[0].current_sprite.position.x = x_position + objects[0].generic_sprite_1.image.get_width()/4
            objects[0].current_sprite.position.y = y_position + objects[0].generic_sprite_1.image.get_height()/4

            x_position += 64
            self.ui_elements.append(objects[0])
        
  