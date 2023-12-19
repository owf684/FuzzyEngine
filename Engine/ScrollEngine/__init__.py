import sys
import pygame
sys.path.append("./objects")
import enemy_object
import player_object

from copy import deepcopy


class ScrollEngine:

    def __init__(self):
        display_info = pygame.display.Info()
        self.screen_width = int(display_info.current_w)
        self.screen_height = int(display_info.current_h * .87)
        self.displacement_x = 0
        self.scroll_offset = 0
        self.scroll_threshold_right = self.screen_width * .4
        self.scroll_threshold_left = self.screen_width * .2

        self.scrolling = False

    def update(self, **kwargs):
        objects = kwargs['GameObject']

        if isinstance(objects, player_object.PlayerObject):
            if objects.physics.position.x > self.scroll_threshold_right and objects.physics.direction.x > 0 or \
                    objects.physics.position.x < self.scroll_threshold_left and objects.physics.direction.x < 0:

                self.scrolling = True
            elif objects.physics.direction.x == 0 and int(abs(objects.physics.velocity.x)) < 0.5:
                self.scrolling = False

            if self.scrolling:
                self.displacement_x = objects.physics.displacement.x
                self.scroll_offset += self.displacement_x

                objects.physics.pause_x_position = True
            else:
                objects.physics.pause_x_position = False

    def scroll_objects(self, **kwargs):

        game_objects = kwargs['GameObjects']
        level_editor = kwargs['LevelEditor']
        input_dict = kwargs['InputDict']
        if self.scrolling and not level_editor.edit:

            for objects in game_objects:
                if not isinstance(objects, player_object.PlayerObject):
                    if objects.physics.pause:

                        objects.physics.position.x -= self.displacement_x
                    else:
                        objects.physics.initial_position.x -= self.displacement_x

        if level_editor.edit and level_editor.scroll_in_edit:
            if abs(input_dict['horizontal']) > 0:
                if input_dict['l-shift'] == 1:
                    self.displacement_x = 5*input_dict['horizontal']
                else:
                    self.displacement_x = 1*input_dict['horizontal']
                self.scroll_offset += self.displacement_x
                for objects in game_objects:
                    if objects.physics.pause:

                        objects.physics.position.x -= self.displacement_x
                        objects.current_sprite.update(objects.physics.position)

                    else:
                        objects.physics.initial_position.x -= self.displacement_x
                        objects.current_sprite.update(objects.physics.initial_position)

        if level_editor.grid.reset_scroll:
            self.scroll_offset = 0
            level_editor.grid.reset_scroll = False
        else:
            level_editor.grid.scroll_offset = deepcopy(self.scroll_offset)
