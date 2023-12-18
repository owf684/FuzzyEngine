import pygame


class Button:

    def __init__(self, text, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = pygame.Rect(x, y, w, h)
        self.back_rect = pygame.Rect(x - 2, y - 2, w + 4, h + 4)
        self.unselected_color = (40, 40, 40)
        self.hover_color = (70, 70, 70)
        self.selected_color = (80, 80, 80)
        self.text = text
        self.font_size = 12
        self.font = pygame.font.Font(None, self.font_size)
        self.font_color = (255, 255, 255)
        self.text_image = self.font.render(self.text, 1, self.font_color)
        self.text_rect = pygame.Rect(x + w / 2 - self.text_image.get_width() / 2,
                                     y + h / 2 - self.text_image.get_height() / 2
                                     , w
                                     , h)
        self.linked_function = None
        self.function_triggered = False
        self.button_pressed = False
        self.hover = False

    def update(self, screen):
        self.detect_input()
        self.trigger_function()
        self.draw(screen)

    def detect_input(self):
        mouse_position = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()
        if self.rect.collidepoint(mouse_position) and mouse_buttons[0]:
            self.button_pressed = True
        elif self.rect.collidepoint(mouse_position):
            self.hover = True
        else:
            self.hover = False
            self.button_pressed = False

    def trigger_function(self):
        if self.button_pressed and not self.function_triggered:
            if self.linked_function is not None:
                self.linked_function()
            self.function_triggered = True
        elif not self.button_pressed and self.function_triggered:
            self.function_triggered = False

    def draw(self, screen):

        if self.button_pressed:
            color = self.selected_color
        elif self.hover:
            color = self.hover_color
        else:
            color = self.unselected_color

        pygame.draw.rect(screen, color, self.rect)
        screen.blit(self.text_image, self.text_rect)

    def set_text(self, text_input):
        self.text_image = self.font.render(self.text, 1, self.font_color)
        while self.text_image.get_width() > self.w:
            self.text = self.text[:len(self.text) - 1]
            self.text_image = self.font.render(self.text, 1, self.font_color)

        self.text_rect = pygame.Rect(self.x + self.w / 2 - self.text_image.get_width() / 2,
                                     self.y + self.h / 2 - self.text_image.get_height() / 2
                                     , self.w
                                     , self.h)

    def connect(self, function):
        self.linked_function = function
