import copy

import pygame
import sys

sys.path.append("./Objects/components")
from vector import Vector

global ENTRY_IMAGE
ENTRY_IMAGE = 0
global RECT
RECT = 1
global VALUE
VALUE = 2
global COLOR
COLOR = 3
global DIRECTORY
DIRECTORY = 4


class ComboBoxUIComponent:

    def __init__(self, width, height):
        self.entries = list()
        self.show_entries = False
        self.font = pygame.font.Font(None, 24)
        self.font_color = (255, 255, 255)
        self.position = Vector(0, 0)
        self.combo_box_color = (100, 100, 100)
        self.entry_selected_color = (50, 50, 50)
        self.entry_unselected_color = (100, 100, 100)
        self.y_gap = 0
        self.selected_index = 0
        self.width = width
        self.height = height
        self.sensing_rect = None
        self.render = False

        self.scroll_value = None
        self.is_scrolling = False
        self.scroll_value_copied = False
        self.scroll_timer_started = False
        self.start_ticks = None
        self.time_elapsed = 0
        self.scroll_entry = None
        self.scroll_entry_copied = False

    def reset(self):
        self.entries.clear()
        self.y_gap = 0
        self.selected_index = 0

    def draw_combo_box(self, screen):
        if len(self.entries) > 0:

            if not self.show_entries:
                pygame.draw.rect(screen, self.entries[self.selected_index][COLOR], self.sensing_rect)
                pygame.draw.rect(screen, (30, 30, 30), self.entries[0][RECT], 2)
                screen.blit(self.entries[self.selected_index][ENTRY_IMAGE],
                            (self.position.x + 5, self.position.y + self.entries[self.selected_index][RECT].height / 4))
            elif self.show_entries:
                y_position = self.position.y

                for entry in self.entries:
                    pygame.draw.rect(screen, entry[COLOR], entry[RECT])
                    pygame.draw.rect(screen, (30, 30, 30), entry[RECT], 2)
                    screen.blit(entry[ENTRY_IMAGE],
                                (self.position.x + 5, y_position + self.entries[self.selected_index][RECT].height / 4))
                    y_position += self.height

    def set_position(self, position_vector):
        self.position = position_vector
        self.sensing_rect = pygame.Rect(position_vector.x, position_vector.y, self.width, self.height)

    def get_value(self):
        return self.entries[self.selected_index][VALUE]

    def get_directory(self):
        return self.entries[self.selected_index][DIRECTORY]

    def add_entry(self, input, directory=''):

        view_input = copy.deepcopy(input)
        entry_image = self.font.render(view_input, 1, self.font_color)

        while entry_image.get_width() > self.width - 5:
            view_input = view_input[:len(view_input) - 1]
            entry_image = self.font.render(view_input, 1, self.font_color)

        rect = pygame.Rect(self.position.x, self.position.y + self.y_gap, self.width, self.height)
        self.y_gap += self.height
        self.entries.append([entry_image, rect, input, self.entry_unselected_color, directory])

    def truncate_image(self, entry):
        value_copy = copy.deepcopy(entry[VALUE])
        while entry[ENTRY_IMAGE].get_width() > self.width - 5:
            value_copy = value_copy[:len(value_copy) - 1]
            entry[ENTRY_IMAGE] = self.font.render(value_copy, 1, self.font_color)

    def restore_image(self, entry):
        value_copy = copy.deepcopy(entry[VALUE])
        entry[ENTRY_IMAGE] = self.font.render(value_copy, 1, self.font_color)
        while entry[ENTRY_IMAGE].get_width() > self.width - 5:
            value_copy = value_copy[:len(value_copy) - 1]
            entry[ENTRY_IMAGE] = self.font.render(value_copy, 1, self.font_color)
    def scroll_text(self, entry):

        if self.scroll_entry_copied and self.scroll_entry != entry:
            self.scroll_entry_copied = False
            self.scroll_value_copied = False
            self.scroll_timer_started = False
            restore_image = self.font.render(self.scroll_entry[VALUE],1, self.font_color)
            self.scroll_entry[ENTRY_IMAGE] = restore_image
            self.truncate_image(self.scroll_entry)

        if not self.scroll_entry_copied:
            self.scroll_entry = entry
            self.scroll_entry_copied = True

        if not self.scroll_timer_started:
            self.start_ticks = pygame.time.get_ticks()
            self.scroll_timer_started = True

        if not self.scroll_value_copied:
            self.scroll_value_copied = True
            self.scroll_value = copy.deepcopy(entry[VALUE])

        seconds = (pygame.time.get_ticks() - self.start_ticks) / 1000

        if seconds > 0.1:
            self.scroll_value = self.scroll_value[1:]
            scroll_image = self.font.render(self.scroll_value, 1, self.font_color)
            entry[ENTRY_IMAGE] = scroll_image
            self.truncate_image(entry)
            self.start_ticks = pygame.time.get_ticks()

        if len(self.scroll_value) < 3:
            self.scroll_value_copied = False

    def update(self, **kwargs):
        d_inputs = kwargs['InputDict']
        mouse_position = pygame.mouse.get_pos()

        if len(self.entries) > 0 and self.sensing_rect is not None and self.sensing_rect.collidepoint(mouse_position):
            try:
                self.entries[self.selected_index][COLOR] = self.entry_selected_color

                if d_inputs['left-click'] and not d_inputs['left_click_latch'] and not self.show_entries:
                    self.show_entries = True
                    d_inputs['left_click_latch'] = True

            except Exception as Error:
                print(Error)

        elif len(self.entries) > 0:
            try:

                self.entries[self.selected_index][COLOR] = self.entry_unselected_color
            except Exception as Error:
                print(Error)

        if self.show_entries:

            for entry in self.entries:
                if entry[RECT].collidepoint(mouse_position):
                    entry[COLOR] = self.entry_selected_color

                    if self.width - 15 <= entry[ENTRY_IMAGE].get_width() and not self.is_scrolling:
                        self.is_scrolling = True

                    if self.is_scrolling:
                        self.scroll_text(entry)

                    if d_inputs['left-click'] and not d_inputs['left_click_latch']:

                        self.show_entries = False
                        self.restore_image(entry)
                        self.selected_index = self.entries.index(entry)

                        d_inputs['left_click_latch'] = True

                    elif not d_inputs['left-click'] and d_inputs['left_click_latch']:

                        d_inputs['left_click_latch'] = False

                else:
                    if entry[COLOR] != self.entry_unselected_color:
                        if self.is_scrolling:
                            self.is_scrolling = False
                        self.restore_image(entry)
                        self.scroll_entry_copied = False
                        self.scroll_value_copied = False
                        self.scroll_timer_started = False

                    entry[COLOR] = self.entry_unselected_color
