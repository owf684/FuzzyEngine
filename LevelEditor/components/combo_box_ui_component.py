import pygame
import sys
sys.path.append("./Objects/components")
from vector import Vector

global ENTRY_IMAGE
ENTRY_IMAGE =0
global RECT
RECT = 1
global VALUE 
VALUE = 2
global COLOR
COLOR = 3
global DIRECTORY
DIRECTORY = 4

class ComboBoxUIComponent:

    def __init__(self,width,height):
        self.entries = list()
        self.show_entries = False
        self.font = pygame.font.Font(None,24)
        self.font_color = (255,255,255)
        self.position = Vector(0,0)
        self.combox_box_color = (100,100,100)
        self.entry_selected_color = (50,50,50)
        self.entry_unselected_color = (100,100,100)
        self.y_gap = 0
        self.selected_index = 0
        self.width=width
        self.height=height
        self.sensing_rect = None
        self.render = False

    def reset(self):
        self.entries.clear()
        self.y_gap = 0
        self.selected_index = 0

    def draw_combo_box(self,screen):
        if len(self.entries) > 0:

            if not self.show_entries:
                pygame.draw.rect(screen, self.entries[self.selected_index][COLOR],self.sensing_rect)
                pygame.draw.rect(screen,(30,30,30),self.entries[0][RECT],2)
                screen.blit( self.entries[self.selected_index][ENTRY_IMAGE],(self.position.x+5,self.position.y+self.entries[self.selected_index][RECT].height/4) )
            elif self.show_entries:
                y_position = self.position.y

                for entry in self.entries:
                    pygame.draw.rect(screen, entry[COLOR],entry[RECT])
                    pygame.draw.rect(screen,(30,30,30),entry[RECT],2)
                    screen.blit( entry[ENTRY_IMAGE],(self.position.x+5,y_position+self.entries[self.selected_index][RECT].height/4) )
                    y_position += self.height

    def set_position(self,position_vector):
        self.position = position_vector
        self.sensing_rect = pygame.Rect(position_vector.x,position_vector.y,self.width,self.height)

    def get_value(self):
        return  self.entries[self.selected_index][VALUE]

    def get_directory(self):
        return self.entries[self.selected_index][DIRECTORY]
    
    def add_entry(self,input,directory=''):

        entry_image = self.font.render(input, 1, self.font_color)
        rect = pygame.Rect(self.position.x,self.position.y+self.y_gap,self.width,self.height)
        self.y_gap += self.height
        self.entries.append([entry_image,rect,input,self.entry_unselected_color,directory])

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
                    entry[COLOR]= self.entry_selected_color

                    if d_inputs['left-click'] and not d_inputs['left_click_latch']:
                    
                        self.show_entries = False
                        self.selected_index = self.entries.index(entry)
     
                        d_inputs['left_click_latch'] = True

                    elif not d_inputs['left-click'] and d_inputs['left_click_latch']:
                    
                        d_inputs['left_click_latch'] = False
        
                else:
                    entry[COLOR] = self.entry_unselected_color
            

            