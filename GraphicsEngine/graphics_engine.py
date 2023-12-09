import pygame
import sys

sys.path.append("./Objects")
sys.path.append("./GameData/GameObjects")
import enemy_object
import environment_object
import game_object
import item_object
import scene_object


class GraphicsEngine:

    def __init__(self):
        pygame.init()
        display_info = pygame.display.Info()
        self.screen_width = int(display_info.current_w)
        self.screen_height = int(display_info.current_h * .87)
        self.grid_size = 32
        self.grid_color = (255, 255, 255)
        # scan block
        self.scan_block_position = [0, 0]
        self.scan_block_size = 32
        self.scan_block_color = (255, 255, 255)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        self.image_buffer = list()
        # render buffer
        self.render_buffer = list()
        self.clear_render_buffer = False
        self.cushion = 32
        self.draw_button_ui_flag = False
        self.button_objects = None
        self.draw_colliders = True

        self.scene_objects = list()
        self.enemy_objects = list()
        self.game_objects = list()
        self.environment_objects = list()
        self.item_objects = list()

        pygame.display.set_caption("Fuzzy Engine")

    def update(self, **kwargs):

        # get variables
        e_level_editor = kwargs['LevelEditor']
        self.screen.fill((92, 148, 252))

        if self.clear_render_buffer:
            self.render_buffer.clear()
            self.item_objects.clear()
            self.enemy_objects.clear()
            self.environment_objects.clear()
            self.game_objects.clear()
            self.scene_objects.clear()
            self.clear_render_buffer = False

        for key, value in kwargs.items():
            if 'ObjectsList' in key:
                self.load_render_buffer(value)

        self.draw_objects()

        # draw level editor
        if e_level_editor.edit:
            e_level_editor.grid.draw_grid(self.screen)
            e_level_editor.object_container_ui.draw_object_containers(self.screen)

        e_level_editor.tool_bar.draw_toolbar_2(self.screen)
        e_level_editor.c_scene.draw_scene_previews(self.screen)

        e_level_editor.tool_bar.draw_toolbar(self.screen)

        e_level_editor.attribute_ui.draw_attributes(self.screen)

        e_level_editor.c_object.draw_object_prompt(self.screen)

        for key, button in e_level_editor.l_button_ui_elements.items():
            if button.render:
                button.draw_button(self.screen)

        for text_box in e_level_editor.text_box_ui.l_text_boxes:
            text_box.draw_text_box(self.screen)

        for key, cb in e_level_editor.l_combo_box_ui_elements.items():
            if cb.render:
                cb.draw_combo_box(self.screen)
        pygame.display.flip()

    def load_render_buffer(self, l_objects):

        for objects in l_objects:
            image = objects.current_sprite.image
            if image is not None:
                if (
                        -image.get_width() - self.cushion < objects.physics.position.x < self.screen_width * 0.8 + image.get_width() + self.cushion
                        or - image.get_width() - self.cushion < objects.physics.initial_position.x < self.screen_width * 0.8 + image.get_width() + self.cushion) \
                        and -image.get_height() < objects.physics.position.y < self.screen_height + image.get_height():

                    if not objects.current_sprite.is_rendered:
                        objects.current_sprite.is_rendered = True

                        if isinstance(objects, enemy_object.EnemyObject):
                            self.enemy_objects.append(objects)
                        elif isinstance(objects, environment_object.EnvironmentObject):
                            self.environment_objects.append(objects)
                        elif isinstance(objects, game_object.GameObject):
                            self.game_objects.append(objects)
                        elif isinstance(objects, item_object.ItemObject):
                            self.item_objects.append(objects)
                        elif isinstance(objects, scene_object.SceneObject):
                            self.scene_objects.append(objects)

                        self.render_buffer.append(objects)
                    elif objects.current_sprite.is_rendered and objects.destroy:

                        if isinstance(objects, enemy_object.EnemyObject):
                            self.enemy_objects.remove(objects)
                        elif isinstance(objects, environment_object.EnvironmentObject):
                            self.environment_objects.remove(objects)
                        elif isinstance(objects, game_object.GameObject):
                            self.game_objects.remove(objects)
                        elif isinstance(objects, item_object.ItemObject):
                            self.item_objects.remove(objects)
                        elif isinstance(objects, scene_object.SceneObject):
                            self.scene_objects.remove(objects)

                        self.render_buffer.remove(objects)
                        l_objects.remove(objects)
                else:

                    objects.current_sprite.is_rendered = False
                    if objects in self.render_buffer:
                        self.render_buffer.remove(objects)

                        if isinstance(objects, enemy_object.EnemyObject):
                            self.enemy_objects.remove(objects)
                        elif isinstance(objects, environment_object.EnvironmentObject):
                            self.environment_objects.remove(objects)
                        elif isinstance(objects, game_object.GameObject):
                            self.game_objects.remove(objects)
                        elif isinstance(objects, item_object.ItemObject):
                            self.item_objects.remove(objects)
                        elif isinstance(objects, scene_object.SceneObject):
                            self.scene_objects.remove(objects)

    def draw_objects(self):

        for objects in self.scene_objects:
            self.blit_object(objects)
        for objects in self.environment_objects:
            self.blit_object(objects)
        for objects in self.item_objects:
            self.blit_object(objects)
        for objects in self.enemy_objects:
            self.blit_object(objects)
        for objects in self.game_objects:
            self.blit_object(objects)

        '''for objects in self.render_buffer:
            self.screen.blit(objects.current_sprite.image,
                             (objects.current_sprite.position.x, objects.current_sprite.position.y))
            if self.draw_colliders:
                pygame.draw.rect(self.screen, (0, 255, 0), objects.current_sprite.rect, 2)'''

    def blit_object(self, objects):
        self.screen.blit(objects.current_sprite.image,
                         (objects.current_sprite.position.x, objects.current_sprite.position.y))
        if self.draw_colliders:
            pygame.draw.rect(self.screen, (0, 255, 0), objects.current_sprite.rect, 2)
