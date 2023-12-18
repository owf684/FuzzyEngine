import pygame


class Label:

    def __init__(self, text, x, y, font_size):
        self.x = x
        self.y = y
        self.font_size = font_size
        self.text = text
        self.rect = pygame.Rect(x, y, 0, 0)

        self.font_color = (255, 255, 255)
        self.font = pygame.font.Font(None, font_size)
        self.text_image = self.font.render(self.text, 1, self.font_color)

    def update(self, screen):
        self.draw(screen)

    def draw(self, screen):
        screen.blit(self.text_image, self.rect)

    def set_text(self, input_text):
        self.text = input_text
        self.text_image = self.font.render(self.text, 1, self.font_color)
