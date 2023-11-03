
import pygame


class GridUIComponent:

    def __init__(self):
        self.display_info = pygame.display.Info()
        #self.screen_width = 1536
        #self.screen_height = 769
        self.screen_width = self.display_info.current_w*0.8
        self.screen_height = self.display_info.current_h*0.8 - 10

        self.max_screen_width = self.screen_width
        self.scroll_offset = 0
        self.grid_size = 32
        self.eox = 0
        self.scroll_delta = 0
        self.grid_color = (255,255,255)


    def draw_grid(self, screen):
        for x in range(0,int(self.screen_width)+int(abs(self.scroll_offset)), self.grid_size):
            pygame.draw.line(screen,self.grid_color, (x-self.scroll_offset, 0), (x-self.scroll_offset, self.screen_height))
            self.eox = x - abs(self.scroll_offset)
            self.scroll_delta = self.max_screen_width - self.eox
            self.screen_width += int(abs(self.scroll_offset))
        for y in range(0, int(self.screen_height),self.grid_size):
            pygame.draw.line(screen,self.grid_color,(0,y),(self.screen_width,y))
