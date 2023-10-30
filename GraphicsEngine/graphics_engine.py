import pygame
class GraphicsEngine:

    def __init__(self):
        pygame.init()
        display_info = pygame.display.Info()
        self.screen_width = int(display_info.current_w)
        self.screen_height = int(display_info.current_h*.87)
        self.grid_size = 32
        self.grid_color = (255,255,255)
        #scan block
        self.scan_block_position = [0,0]
        self.scan_block_size = 32
        self.scan_block_color = (255,255,255)
        self.screen = pygame.display.set_mode((self.screen_width,self.screen_height))
        self.image_buffer = list()
        #render buffer
        self.render_buffer = list()
        self.clear_render_buffer = False
        self.cushion = 32
        self.draw_button_ui_flag = False
        self.button_objects = None
        pygame.display.set_caption("Fario Faker")

    def update(self, **kwargs):
        #get variables
        
        e_level_editor = kwargs['LevelEditor']
        self.screen.fill((92,148,252))

        if self.clear_render_buffer:
            self.render_buffer.clear()
            self.clear_render_buffer = False

        for key, value in kwargs.items():
            if 'ObjectsList' in key:
                self.load_render_buffer(value)
           
        #draw scenery first

        #draw environment second

        #draw ui 

        #draw game objects
        self.draw_objects()  

        #draw level editor
        if e_level_editor.edit:
            e_level_editor.grid.draw_grid(self.screen)
            self.draw_object_editor_ui(e_level_editor.object_editor_ui.l_object_editor_ui_elements)


        e_level_editor.tool_bar.draw_attributes(self.screen)    
        self.draw_button_ui(e_level_editor.l_button_ui_elements)



        pygame.display.flip()


    def load_render_buffer(self, l_objects):

        for objects in l_objects:
            image = objects.current_sprite.image
            if  image is not None:
                if (-image.get_width()  - self.cushion < objects.physics.position.x < self.screen_width+image.get_width() + self.cushion ) \
                    or ( -image.get_height() < objects.physics.position.y < self.screen_height + image.get_height()):

                    if not objects.current_sprite.is_rendered:
                        objects.current_sprite.is_rendered = True
                        self.render_buffer.append(objects)         
                else:

                    objects.current_sprite.is_rendered = False
                    if objects in self.render_buffer:
                        self.render_buffer.remove(objects)

    def draw_objects(self):
      for objects in self.render_buffer:
            self.screen.blit(objects.current_sprite.image,(objects.current_sprite.position.x,objects.current_sprite.position.y))

    # rule to remember ui elements can display all 5 sprites at once                
    def draw_object_editor_ui(self,l_ui_elements):

        for objects in l_ui_elements:
            #draw generic sprite 1
            if objects.generic_sprite_1.image is not None:

                self.screen.blit(objects.generic_sprite_1.image,(objects.generic_sprite_1.position.x,objects.generic_sprite_1.position.y))

            #draw generic sprite 2
            if objects.generic_sprite_2.image is not None:

                self.screen.blit(objects.generic_sprite_2.image,(objects.generic_sprite_2.position.x,objects.generic_sprite_2.position.y))

            #draw generic sprite 3
            if objects.generic_sprite_3.image is not None:

                self.screen.blit(objects.generic_sprite_3.image,(objects.generic_sprite_3.position.x,objects.generic_sprite_3.position.y))

            #draw generic sprite 4
            if objects.generic_sprite_4.image is not None:

                self.screen.blit(objects.generic_sprite_4.image,(objects.generic_sprite_4.position.x,objects.generic_sprite_4.position.y))

            #draw current sprite
            if objects.current_sprite.image is not None:

                self.screen.blit(objects.current_sprite.image,(objects.current_sprite.position.x,objects.current_sprite.position.y))

    def draw_button_ui(self,l_ui_elements):
        for key, button in l_ui_elements.items():
            if len(button.sprite.sprite_sheet)>0:
                if button.sprite.sprite_sheet[button.sprite.animation_state] is not None:
                    self.screen.blit(button.sprite.sprite_sheet[button.sprite.animation_state],(button.sprite.position.x,button.sprite.position.y))
