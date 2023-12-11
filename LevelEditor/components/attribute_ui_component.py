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
        self.event = None
        self.scroll_delta = 0

    def draw_attributes(self, screen):

        pygame.draw.rect(screen, self.attr_window_color, (
            self.attr_window_position.x + 130, self.attr_window_position.y, self.display_width / 6.25,
            self.attr_window_size.y))

        self.update_attribute_values(screen)

        pygame.draw.rect(screen, self.attr_window_color, (
            self.attr_window_position.x, self.attr_window_position.y, self.attr_window_size.x, self.attr_window_size.y))

        self.update_attribute_names(screen)

    def update_attribute_names(self, screen):
        x_position = self.display_width + 10
        y_position = self.attr_window_position.y + 10
        y_increment = 25
        x_spacing = 200
        i = 0
        if self.selected_object is not None:

            if hasattr(self.selected_object, "__dict__"):

                for key, value in vars(self.selected_object).items():

                    screen.blit(self.l_attribute_components[i].attribute_image, (x_position, y_position))
                    y_position += y_increment
                    i += 1

    def update_attribute_values(self, screen):
        x_position = self.display_width + 10
        y_position = self.attr_window_position.y + 10
        y_increment = 25
        x_spacing = 200
        i = 0
        if self.selected_object is not None:

            if hasattr(self.selected_object, "__dict__"):

                for key, value in vars(self.selected_object).items():
                    if not self.attributes_created:
                        self.add_attribute_component([key, value], x_position, y_position)

                    x = x_position + x_spacing + self.scroll_delta
                    self.l_attribute_components[i].update_value(value, x)

                    while x < self.attr_window_position.x:
                        value = str(value)[1:]
                        self.l_attribute_components[i].update_value(value,x)
                        x += 2

                    screen.blit(self.l_attribute_components[i].value_image, (x, y_position))
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
                    self.scroll_delta = d_inputs['scroll_delta'] = 0
                elif not d_inputs['left-click'] and d_inputs['left_click_latch']:
                    d_inputs["left_click_latch"] = False

    def update(self, **kwargs):

        self.scroll_attributes()

    def scroll_attributes(self):
        if self.event is not None:
            mouse_position = pygame.mouse.get_pos()
            # update scroll delta
            if mouse_position[0] >= self.attr_window_position.x:
                self.scroll_delta += -1 * self.event.x * 10
                self.event = None

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
                        self.scroll_delta= 0
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
            self.scroll_delta = 0
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
        self.offscreen_value = ''
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

    def update_value(self, value, x):


        mouse_position = pygame.mouse.get_pos()

        self.attr_data[1] = value
        self.value_rect.x = x
        self.value_image = self.font.render(str(self.attr_data[1]), 1, self.font_color)

        self.value_selected_image = self.font.render(str(self.attr_data[1]), 1, self.select_color)

        self.value_unselected_image = self.value_image

        if self.value_rect.collidepoint(mouse_position):

            self.value_image = self.value_selected_image

        else:
            self.value_image = self.value_unselected_image
