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
        self.sprite_path = None
        #sprite sheet
        self.sprite_sheet = list()

        self.elapsed_time = 0
        self.current_time = 0 
        self.last_frame_time = 0
        self.frame_index = 0
        self.frame_duration = 0
        self.frame_count = 0
        self.animation_state = 0
    def create_sprite(self,sprite_path):
        try:
            self.sprite_path = sprite_path
            self.image = pygame.image.load(sprite_path).convert_alpha()
            if self.image is not None:
                self.mask = pygame.mask.from_surface(self.image)
                x,y = self.image.get_size()
                self.image_size.x = x
                self.image_size.y = y

                self.rect = pygame.Rect(self.position.x,self.position.y,self.image_size.x,self.image_size.y)
      
        except Exception as Error:
            print("ERROR: ", Error)

    def create_sprite_sheet(self,sprite_path,frame_count,frame_size):
        try:
            self.sprite_path = sprite_path
            self.sprite_sheet.clear()
            sprite_sheet = pygame.image.load(sprite_path).convert_alpha()
            for i in range(frame_count):
                frame = sprite_sheet.subsurface((0, i*frame_size.y, frame_size.x,frame_size.y))
                self.sprite_sheet.append(frame)

        except Exception as Error:
            print("ERROR::anim_util.py::extract_frames", Error)        
      
    def create_sprite_sheet_rect(self):
        if len(self.sprite_sheet) > 0:
            self.rect =pygame.Rect(self.position.x,self.position.y,self.sprite_sheet[self.animation_state].get_width(),self.sprite_sheet[self.animation_state].get_height())
            self.image_size.x = self.sprite_sheet[self.animation_state].get_width()
            self.image_size.y = self.sprite_sheet[self.animation_state].get_height()

    def determine_frame_count(self):
        try:
             
            self.current_time = pygame.time.get_ticks()
            self.elapsed_time = self.current_time - self.last_frame_time

            if self.elapsed_time >= self.frame_duration:
                self.frame_index = (self.frame_index + 1) % self.frame_count
                self.last_frame_time = self.current_time

        except Exception as Error:
            print("ERROR::anim_util.py::determine_frame_count", Error)
            
    def update(self,position,rect=None):
        self.position = position()
        if rect is not None:
            self.rect = pygame.Rect(self.position.x,self.position.y,rect.x,rect.y)
        else:
            self.rect = pygame.Rect(self.position.x,self.position.y,self.image_size.x,self.image_size.y)
        
            
def create_object():
    return SpriteComponent()