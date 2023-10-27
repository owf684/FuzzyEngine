import pygame
from vector import Vector
class SpriteComponent:

    def __init__(self):

        self.image = None
        self.rect = None
        self.mask = None
        self.image_size = Vector(0,0)
        self.position = Vector(0,0)
        self.is_rendered = False

    def create_sprite(self,sprite_path):
        try:

            self.image = pygame.image.load(sprite_path).convert_alpha()
            if self.image is not None:
                self.mask = pygame.mask.from_surface(self.image)
                self.image_size = self.image.get_size()
                self.rect = pygame.Rect(self.position.x,self.position.y,self.image_size[0],self.image_size[1])
      
        except Exception as Error:
            print("ERROR: ", Error)

def create_object():
    return SpriteComponent()