import sys
import pygame
sys.path.append('./GameData/GameObjects')
import player_object



class ScrollEngine:

    def __init__(self):
        display_info = pygame.display.Info()
        self.screen_width = int(display_info.current_w)
        self.screen_height = int(display_info.current_h*.87)
        self.displacement_x = 0
        self.scroll_offset = 0
        self.scroll_threshold_right = self.screen_width*.4
        self.scroll_threshold_left = self.screen_width*.2

        self.scrolling = False

    def update(self, **kwargs):
        objects = kwargs['GameObject']

        if isinstance(objects,player_object.PlayerObject):
            if objects.physics.position.x > self.scroll_threshold_right and objects.physics.direction.x > 0 or \
                objects.physics.position.x < self.scroll_threshold_left and objects.physics.direction.x < 0:

                self.scrolling = True
            else:
                self.scrolling = False
          
            if self.scrolling:
                self.displacement_x = objects.physics.displacement.x
                self.scroll_offset += self.displacement_x
                  
                objects.physics.pause_x_position = True
            else:
                objects.physics.pause_x_position = False



    def scroll_objects(self,**kwargs):

        game_objects = kwargs['GameObjects']
        level_editor = kwargs['LevelEditor']

        if self.scrolling:

            for objects in game_objects:
                if not isinstance(objects,player_object.PlayerObject):
                    objects.physics.position.x -= self.displacement_x

        level_editor.grid.scroll_offset = self.scroll_offset
              
    