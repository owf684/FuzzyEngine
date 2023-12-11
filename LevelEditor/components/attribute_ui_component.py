import sys
import pygame

sys.path.append("./Objects/components")
from vector import Vector
import text_box_ui_component


class AttributeUIComponent:

    def __init__(self):
        self.display_info = pygame.display.Info()
        self.display_width = int(self.display_info.current_w * .8)
        self.display_height = int(self.display_info.current_h * .8)

        self.attr_window_color = (70, 70, 70)
        self.attr_window_position = Vector(self.display_width + 5, 200)
        self.attr_window_size = Vector(130, self.display_height - 25)

        self.font = pygame.font.Font(None, 18)
        self.font_color = (255, 255, 255)
        self.font_size = 0.5

        self.l_attributes = list()
        self.l_previous_attributes = list()
        self.l_attribute_components = list()
        self.l_previous_attribute_components = list()
        self.l_text_boxes = list()
        self.selected_object = None
        self.previous_object = list()
        self.attributes_created = False

    def draw_attributes(self, screen):

        pygame.draw.rect(screen, self.attr_window_color, (
        self.attr_window_position.x, self.attr_window_position.y, self.attr_window_size.x, self.attr_window_size.y))
        pygame.draw.rect(screen, self.attr_window_color, (
        self.attr_window_position.x + 130, self.attr_window_position.y, self.display_width / 6.25,
        self.attr_window_size.y))
        self.update_attributes(screen)

    def update_attributes(self, screen):
        x_position = self.display_width + 10
        y_position = self.attr_window_position.y + 10
        y_increment = 25
        x_spacing = 150
        i = 0
        if self.selected_object is not None:

            if hasattr(self.selected_object, "__dict__"):

                for key, value in vars(self.selected_object).items():
                    if not self.attributes_created:
                        self.add_attribute_component([key, value], x_position, y_position)

                    self.l_attribute_components[i].update_value(value)

                    screen.blit(self.l_attribute_components[i].attribute_image, (x_position, y_position))
                    screen.blit(self.l_attribute_components[i].value_image, ((x_position + x_spacing), y_position))
                    y_position += y_increment
                    i += 1
                if not self.attributes_created and len(self.l_attribute_components) > 0:
                    self.attributes_created = True

    def update_selected_object(self, d_inputs, game_objects):
        mouse_position = pygame.mouse.get_pos()

        for objects in game_objects:
            if objects.current_sprite.rect.collidepoint(mouse_position):
                if d_inputs['left-click'] and not d_inputs['left_click_latch']:
                    d_inputs['left_click_latch'] = True

                    self.selected_object = objects
                    self.attributes_created = False
                    self.l_attribute_components.clear()
                elif not d_inputs['left-click'] and d_inputs['left_click_latch']:
                    d_inputs["left_click_latch"] = False

    def update_object_attributes(self, d_input):
        mouse_position = pygame.mouse.get_pos()

        for attr in self.l_attribute_components:

            if attr.value_rect.collidepoint(mouse_position):

                if d_input['left-click'] and not d_input['left_click_latch']:

                    if hasattr(attr.attr_data[1], '__dict__'):
                        self.l_attribute_components.clear()
                        self.attributes_created = False
                        self.previous_object.append(self.selected_object)
                        self.selected_object = attr.attr_data[1]

                    d_input['left_click_latch'] = True

                elif not d_input['left-click'] and d_input['left_click_latch']:

                    d_input['left_click_latch'] = False

    def add_attribute_component(self, attr, x, y):
        self.l_attribute_components.append(AttributeComponent())
        self.l_attribute_components[-1].create_attribute(attr, Vector(x, y))

    def restore_attribute_components(self):
        if len(self.previous_object) > 0:
            self.selected_object = self.previous_object.pop()
            self.l_attribute_components.clear()
            self.attributes_created = False
            self.l_text_boxes.clear()


class AttributeComponent:

    def __init__(self):

        self.position = Vector(0, 0)
        self.attr_data = None
        self.attribute_image = None
        self.value_image = None
        self.value_selected_image = None
        self.value_unselected_image = None
        self.attribute_rect = None
        self.value_rect = None
        self.font = pygame.font.Font(None, 18)
        self.font_color = (255, 255, 255)
        self.select_color = (0, 50, 225)
        self.x_spacing = 150
        self.y_increment = 25

    def create_attribute(self, attr, position):
        self.attr_data = attr
        self.position = position

        self.attribute_image = self.font.render(str(attr[0]), 1, self.font_color)

        self.value_image = self.font.render(str(attr[1])[:34], 1, self.font_color)

        self.value_selected_image = self.font.render(str(attr[1])[:34], 1, self.select_color)

        self.attribute_rect = pygame.Rect(self.position.x, self.position.y, self.attribute_image.get_width(),
                                          self.attribute_image.get_height())

        self.value_rect = pygame.Rect(self.position.x + self.x_spacing, self.position.y, self.value_image.get_width(),
                                      self.value_image.get_height())

        self.value_unselected_image = self.value_image

    def update_value(self, value):

        mouse_position = pygame.mouse.get_pos()

        self.attr_data[1] = value

        self.value_image = self.font.render(str(self.attr_data[1]), 1, self.font_color)

        self.value_selected_image = self.font.render(str(self.attr_data[1]), 1, self.select_color)

        self.value_unselected_image = self.value_image

        if self.value_rect.collidepoint(mouse_position):

            self.value_image = self.value_selected_image

        else:
            self.value_image = self.value_unselected_image
