import pygame
import sys
sys.path.append("./Objects/components")
from vector import Vector

global BGCOLOR, PRINT_EVENT, CHATBOX_POS, CHATLIST_POS, CHATLIST_MAXSIZE


ChatList = []
class TextBoxUIComponent:

    def __init__(self):
        pygame.key.start_text_input()

        self.l_text_boxes = list()
        self.selected_text_box = None
        self.PRINT_EVENT = True
        self.ChatList= []
        self._IMEEditing = False
        self._IMEText = ""
        self._IMETextPos = 0
        self._IMEEditingText = ""
        self._IMEEditingPos = 0

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

        self.IMETEXT()
        print(self._IMEText)
    def IMETEXT(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            elif event.type == pygame.KEYDOWN:

                if self._IMEEditing:
                    if len(self._IMEEditingText) == 0:
                        self._IMEEditing = False
                    continue

                if event.key == pygame.K_BACKSPACE:
                    if len(self._IMEText) > 0 and self._IMETextPos > 0:
                        self._IMEText = (
                            self._IMEText[0 : self._IMETextPos - 1] + self._IMEText[self._IMETextPos:]
                        )
                        self._IMETextPos = max(0, self._IMETextPos - 1)

                elif event.key == pygame.K_DELETE:
                    self._IMEText = self._IMEText[0:self._IMETextPos] + self._IMEText[self._IMETextPos + 1 :]
                elif event.key == pygame.K_LEFT:
                    self._IMETextPos = max(0, self._IMETextPos - 1)
                elif event.key == pygame.K_RIGHT:
                    self._IMETextPos = min(len(self._IMEText), self._IMETextPos + 1)

                elif (
                    event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]
                    and len(event.unicode) == 0
                ):
                    # Block if we have no text to append
                    if len(self._IMEText) == 0:
                        continue

                    # Append chat list
                    ChatList.append(self._IMEText)
                    if len(ChatList) > CHATLIST_MAXSIZE:
                        ChatList.pop(0)
                    self._IMEText = ""
                    self._IMETextPos = 0

            elif event.type == pygame.TEXTEDITING:
                if self.PRINT_EVENT:
                    print(event)
                self._IMEEditing = True
                self._IMEEditingText = event.text
                self._IMEEditingPos = event.start

            elif event.type == pygame.TEXTINPUT:
                if self.PRINT_EVENT:
                    print(event)
                self._IMEEditing = False
                self._IMEEditingText = ""
                self._IMEText = self._IMEText[0:self._IMETextPos] + event.text + self._IMEText[self._IMETextPos:]
                self._IMETextPos += len(event.text)


class TextBox:

    def __init__(self,width,height,Vector):
        self.position = Vector
        self.width = width
        self.height = height
        self.userInput = ''
        self.selected = False
        self.rect = pygame.Rect(self.position.x,self.position.y,self.width,self.height)
        pygame.key.start_text_input()
        pygame.key.set_text_input_rect(self.rect)
    def draw_text_box(self,screen):
        pygame.draw.rect(screen,(255,0,0),self.rect,2)


