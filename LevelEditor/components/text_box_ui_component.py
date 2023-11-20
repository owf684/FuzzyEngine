import pygame
import sys
import pygame.freetype as freetype
sys.path.append("./Objects/components")
from vector import Vector


ChatList = []
class TextBoxUIComponent:

    def __init__(self):
        pygame.key.start_text_input()

        self.l_text_boxes = list()
        self.previos_attribute_components = list()
        self.selected_text_box = None
        self.input_text = ''
        self.event = None

    def get_input(self,**kwargs):
        d_input = kwargs['InputDict']
        mouse_position = pygame.mouse.get_pos()
        for text_box in self.l_text_boxes:
            if text_box.rect.collidepoint(mouse_position):
                if d_input['left-click']:
                    if text_box != self.selected_text_box:
                        if self.selected_text_box is not None:
                            self.selected_text_box.selected = False
                            self.selected_text_box.text_box_color = text_box.unselected_color
                        text_box.selected = True
                        text_box.text_box_color =text_box.selected_color
                        self.selected_text_box = text_box
                        self.input_text = self.selected_text_box.userInput 
        self.handle_input_events()

    def handle_input_events(self):
        if self.event is None:
            return
    
        if self.selected_text_box is not None:

            match self.event.type:
        
                case pygame.TEXTINPUT:
    
                    self.input_text += self.event.text

                case pygame.KEYDOWN:

                    match self.event.key:

                        case pygame.K_BACKSPACE:
                            self.input_text = self.input_text[:len(self.input_text)-1]

                    
                        case pygame.K_RETURN:
                            if len(self.selected_text_box.userInput) > 0:
                                self.selected_text_box.linked_attr.attr_data[1] = float(self.selected_text_box.userInput)
                                
                                self.l_text_boxes.remove(self.selected_text_box)

            self.selected_text_box.userInput = self.input_text
        # clear event or else it'll keep adding the same key
        self.event = None

        #self.read_input()
    def read_input(self):

        print(self.input_text)


class TextBox:

    def __init__(self,width,height,Vector):
        self.position = Vector
        self.width = width
        self.height = height
        self.userInput = ''
        self.selected = False
        self.rect = pygame.Rect(self.position.x,self.position.y,self.width,self.height)
        self.linked_attr = None
        self.font_names = [
        "notosanscjktcregular",
        "notosansmonocjktcregular",
        "notosansregular,",
        "microsoftjhengheimicrosoftjhengheiuilight",
        "microsoftyaheimicrosoftyaheiuilight",
        "msgothicmsuigothicmspgothic",
        "msmincho",
        "Arial",
        ]
        self.selected_color = (100,100,100)
        self.unselected_color = (150,150,150)
        self.text_box_color = (150,150,150)
        self.font_small = freetype.SysFont(self.font_names, 12)

        pygame.key.start_text_input()
        pygame.key.set_text_input_rect(self.rect)
    def draw_text_box(self,screen):
        pygame.draw.rect(screen,self.text_box_color,self.rect)
        pygame.draw.rect(screen,(50,50,50),self.rect,2)
        text_rect= pygame.Rect(self.rect.x+5,self.rect.y+self.rect.height/2,self.rect.width,self.rect.height)
        if len(self.userInput)*7 > self.rect.width:
            userInput = self.userInput[:self.rect.width//7]
        else:
            userInput = self.userInput
        self.font_small.render_to(screen, text_rect, userInput, (255,255,255))


