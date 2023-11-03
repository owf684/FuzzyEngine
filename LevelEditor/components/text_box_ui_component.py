import pygame
import sys
import pygame.freetype as freetype
sys.path.append("./Objects/components")
from vector import Vector

global BGCOLOR, PRINT_EVENT, CHATBOX_POS, CHATLIST_POS, CHATLIST_MAXSIZE


ChatList = []
class TextBoxUIComponent:

    def __init__(self):
        pygame.key.start_text_input()

        self.l_text_boxes = list()
        self.selected_text_box = None
        self.input_text = ''
        self.event = None

    def get_input(self):
        mouse_position = pygame.mouse.get_pos()
        for text_box in self.l_text_boxes:
            if text_box.rect.collidepoint(mouse_position):
                if pygame.MOUSEBUTTONDOWN:
                    if text_box != self.selected_text_box:
                        if self.selected_text_box is not None:
                            self.selected_text_box.selected = False
                        text_box.selected = True
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

        self.read_input()
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
        self.font_small = freetype.SysFont(self.font_names, 12)

        pygame.key.start_text_input()
        pygame.key.set_text_input_rect(self.rect)
    def draw_text_box(self,screen):
        pygame.draw.rect(screen,(255,255,255),self.rect)
        self.font_small.render_to(screen, self.rect, self.userInput, (0,0,0))


