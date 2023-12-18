import copy
import pygame

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


class ComboBox:

    def __init__(self, combo_box_name, x, y, width, height):
        self.index_offset = 0
        self.entries = list()
        self.show_entries = False
        self.font = pygame.font.Font(None, 18)
        self.font_color = (255, 255, 255)

        self.name = combo_box_name
        self.position = Vector(x, y)
        self.sensing_rect = pygame.Rect(x, y, width, height)

        self.combo_box_color = (100, 100, 100)
        self.entry_selected_color = (50, 50, 50)
        self.entry_unselected_color = (100, 100, 100)
        self.y_gap = 0
        self.selected_index = 0
        self.last_selected_index = -1

        self.width = width
        self.height = height
        self.render = True

        self.linked_function = None
        self.trigger_on_change = False

        self.scroll_value = None
        self.is_scrolling = False
        self.scroll_value_copied = False
        self.scroll_timer_started = False
        self.start_ticks = None
        self.time_elapsed = 0
        self.scroll_entry = None
        self.scroll_entry_copied = False
        self.left_click_latch = False
        self.scroll_up_buffer = list()
        self.scroll_down_buffer = list()
        self.scroll_offset_y = 0

    # resets combo box
    def reset(self):
        self.entries.clear()
        self.y_gap = 0
        self.selected_index = 0
        self.index_offset = -1
        self.last_selected_index = -1
        self.add_entry('None')


    # returns the true index of the combo box
    def get_index(self):

        return self.selected_index + self.index_offset

    def draw_combo_box(self, screen):
        if len(self.entries) > 0:

            if not self.show_entries:
                pygame.draw.rect(screen, self.entries[self.selected_index][COLOR], self.sensing_rect)
                pygame.draw.rect(screen, (30, 30, 30), self.entries[0][RECT], 2)
                screen.blit(self.entries[self.selected_index][ENTRY_IMAGE],
                            (self.position.x + 5, self.position.y + self.entries[self.selected_index][RECT].height / 4))

            elif self.show_entries:
                y_position = self.position.y

                i = 0
                for entry in self.entries:
                    pygame.draw.rect(screen, entry[COLOR], entry[RECT])
                    pygame.draw.rect(screen, (30, 30, 30), entry[RECT], 2)
                    screen.blit(entry[ENTRY_IMAGE],
                                (self.position.x + 5, y_position + self.entries[self.selected_index][RECT].height / 4))
                    y_position += self.height
                    i += 1

                    if i == 10:
                        break

    def on_change(self):
        if self.trigger_on_change:
            if self.linked_function is not None:
                if self.selected_index != self.last_selected_index:
                    self.last_selected_index = self.selected_index
                    self.linked_function(name=self.name)
                    return True
        return False

    def set_position(self, position_vector):
        self.position = position_vector
        self.sensing_rect = pygame.Rect(position_vector.x, position_vector.y, self.width, self.height)

    def get_value(self):
        return self.entries[self.selected_index][VALUE]

    def get_directory(self):
        return self.entries[self.selected_index][DIRECTORY]

    def add_entry(self, input_text, directory=''):

        view_input = copy.deepcopy(input_text)
        entry_image = self.font.render(view_input, 1, self.font_color)

        while entry_image.get_width() > self.width - 5:
            view_input = view_input[:len(view_input) - 1]
            entry_image = self.font.render(view_input, 1, self.font_color)

        rect = pygame.Rect(self.position.x, self.position.y + self.y_gap + self.scroll_offset_y, self.width,
                           self.height)
        self.y_gap += self.height
        self.entries.append([entry_image, rect, input_text, self.entry_unselected_color, directory])

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
            restore_image = self.font.render(self.scroll_entry[VALUE], 1, self.font_color)
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

    def update(self, screen, events, combo_boxes):

        mouse_position = pygame.mouse.get_pos()
        mouse_button = pygame.mouse.get_pressed()

        if len(self.entries) > 0 and self.sensing_rect is not None and self.sensing_rect.collidepoint(mouse_position):
            try:
                self.entries[self.selected_index][COLOR] = self.entry_selected_color

                if mouse_button[0] and not self.left_click_latch and not self.show_entries:
                    self.show_entries = True
                    self.left_click_latch = True
                elif not mouse_button[0] and self.left_click_latch:
                    self.left_click_latch = False

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

                    if mouse_button[0] and not self.left_click_latch:

                        self.show_entries = False
                        self.restore_image(entry)
                        self.selected_index = self.entries.index(entry)

                        self.left_click_latch = True

                    elif not mouse_button[0] and self.left_click_latch and not self:

                        self.left_click_latch = False

                else:
                    if entry[COLOR] != self.entry_unselected_color:
                        if self.is_scrolling:
                            self.is_scrolling = False
                        self.restore_image(entry)
                        self.scroll_entry_copied = False
                        self.scroll_value_copied = False
                        self.scroll_timer_started = False

                    entry[COLOR] = self.entry_unselected_color
        if self.show_entries:
            self.scroll_entries(events)
        self.draw_combo_box(screen)

        if self.on_change():
            return True
        else:
            return False

    def scroll_entries(self, events):
        if events['MouseWheel'] is not None:
            if events['MouseWheel'].y == 1:
                if len(self.entries) > 10:

                    for entry in self.entries:
                        entry[RECT].y -= self.height

                    self.scroll_offset_y -= self.height

                    self.scroll_down_buffer.append(self.entries[0])
                    self.entries = self.entries[1:]
                    self.index_offset += 1
            if events['MouseWheel'].y == -1:
                if len(self.scroll_down_buffer) > 0:

                    self.entries.insert(0, self.scroll_down_buffer.pop())
                    self.index_offset -= 1

                    for entry in self.entries:
                        entry[RECT].y += self.height
                    self.scroll_offset_y += self.height

    def connect(self, function, trigger_on_change):
        self.linked_function = function
        self.trigger_on_change = trigger_on_change
