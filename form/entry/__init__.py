import copy

import pygame


class Entry:

    def __init__(self, x, y, w, h, font_size):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.rect = pygame.Rect(x, y, w, h)
        self.color = (125, 125, 125)
        self.selected_color = (80, 80, 80)
        self.active_color = self.color
        self.back_color = (50, 50, 50)
        self.back_rect = pygame.Rect(x - 2, y - 2, w + 4, h + 4)
        self.active = False
        self.input = ''
        self.cursor = '|'
        self.font_color = (255, 255, 255)
        self.font_size = font_size
        self.font = pygame.font.Font(None, font_size)

        self.event = None

        self.start_tick_recorded = False
        self.start_tick = 0
        self.add_cursor = False

    def update(self, screen, events):
        self.event = events
        self.get_input()
        if self.active:
            self.handle_cursor()
        self.draw(screen)

        self.event = None

    def get_input(self):
        mouse_position = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()

        if self.rect.collidepoint(mouse_position):
            if mouse_buttons[0]:
                self.active = True
                self.active_color = self.selected_color
        elif not self.rect.collidepoint(mouse_position):
            if mouse_buttons[0]:
                self.active = False
                self.active_color = self.color
                if self.add_cursor:
                    self.input = self.input.rstrip(self.cursor)
        if self.active:
            self.handle_input_events()

    def handle_input_events(self):
        if self.event['TextInput'] is not None:

            if self.add_cursor:
                self.input = self.input.rstrip(self.cursor)
                self.input += self.event['TextInput'].text
                self.input += self.cursor
            else:
                self.input += self.event['TextInput'].text

        if self.event['KeyDown'] is not None:

            match self.event['KeyDown'].key:

                case pygame.K_BACKSPACE:
                    self.input = self.input[:len(self.input) - 1]

                case pygame.K_RETURN:
                    if self.add_cursor:
                        self.input = self.input.rstrip(self.cursor)
                        self.add_cursor = False

                    self.active = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.back_color, self.back_rect)
        pygame.draw.rect(screen, self.active_color, self.rect)
        text_image = self.font.render(self.input, 1, self.font_color)
        input_copy = copy.deepcopy(self.input)
        while text_image.get_width() > self.w:
            input_copy = input_copy[1:]
            text_image = self.font.render(input_copy, 1, self.font_color)

        text_rect = pygame.Rect(self.x, self.y + text_image.get_height() / 2, self.w, self.h)
        screen.blit(text_image, text_rect)

    def handle_cursor(self):
        if not self.start_tick_recorded:
            self.start_tick = pygame.time.get_ticks()
            self.start_tick_recorded = True

        seconds = (pygame.time.get_ticks() - self.start_tick) / 1000

        if seconds > .5:
            if not self.add_cursor and self.start_tick_recorded:
                self.add_cursor = True
                self.input += self.cursor
                self.start_tick_recorded = False

            if self.add_cursor and self.start_tick_recorded:
                self.input = self.input.rstrip(self.cursor)
                self.add_cursor = False
                self.start_tick_recorded = False

    def get_text(self):
        if self.add_cursor:
            self.input = self.input.rstrip(self.cursor)
        return self.input
