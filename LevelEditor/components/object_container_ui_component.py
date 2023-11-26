import pygame
import sys

class ObjectContainerUIComponent:

    def __init__(self):
        self.l_object_editor_ui_elements = list()
        display_info = pygame.display.Info()
        self.screen_width = int(display_info.current_w*.8)
        self.screen_height = int(display_info.current_h*.8)
        self.object_container_path = './Assets/UI/Containers/ObjectContainer.png'
        self.object_container_selected_path = './Assets/UI/Containers/ObjectContainer_selected.png'

    def init_ui(self,c_object_creator):
        self.l_object_editor_ui_elements.clear()

        for category in c_object_creator.l_categories:
            y_position =25
            x_position = (self.screen_width/2) - len(c_object_creator.l_categories[c_object_creator.i_category])*64/3
            for objects in category:
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
                self.l_object_editor_ui_elements.append(objects[0])

                # clear generic sprites. these are non-ui elements
                objects[0].generic_sprite_2.image = None
                objects[0].generic_sprite_3.image = None
                objects[0].generic_sprite_4.image = None


                c_object_creator.update_editor_ui = True

    def draw_object_containers(self,screen):

      for objects in self.l_object_editor_ui_elements:
            #draw generic sprite 1
            if objects.generic_sprite_1.image is not None:

                screen.blit(objects.generic_sprite_1.image,(objects.generic_sprite_1.position.x,objects.generic_sprite_1.position.y))

            #draw generic sprite 2
            if objects.generic_sprite_2.image is not None:

                screen.blit(objects.generic_sprite_2.image,(objects.generic_sprite_2.position.x,objects.generic_sprite_2.position.y))

            #draw generic sprite 3
            if objects.generic_sprite_3.image is not None:

                screen.blit(objects.generic_sprite_3.image,(objects.generic_sprite_3.position.x,objects.generic_sprite_3.position.y))

            #draw generic sprite 4
            if objects.generic_sprite_4.image is not None:

                screen.blit(objects.generic_sprite_4.image,(objects.generic_sprite_4.position.x,objects.generic_sprite_4.position.y))

            #draw current sprite
            if objects.current_sprite.image is not None:

                screen.blit(objects.current_sprite.image,(objects.current_sprite.position.x,objects.current_sprite.position.y))
  
    def update_object_container_ui(self,c_object_creator):
        try:

            if c_object_creator.update_editor_ui:

                for objects in c_object_creator.get_selected_category():
                    objects[0].generic_sprite_1.create_sprite(self.object_container_path)

                c_object_creator.get_selected_object()[0].generic_sprite_1.create_sprite(self.object_container_selected_path)

                self.l_object_editor_ui_elements.clear()

                for objects in c_object_creator.get_selected_category():
                    self.l_object_editor_ui_elements.append(objects[0])

                c_object_creator.update_editor_ui = False
        except:
            print(c_object_creator.get_selected_object())

