import pygame


class InputsEngine:

    def __init__(self):
        self.hold_create = False
        self.horizontal = 0
        self.vertical = 0
        self.input_dict = {
            "vertical": 0,
            "horizontal" : 0,
            "left-click"	: False,
            "right-click" 	: False,
            "create-level" 	: 0,
            "patch-lev"	: 0,
            "load-lev"	: 0,
            "arrow-vert"	: 0,
            "arrow-hori"	: 0,
            "l_shift"		: 0,
            "edit"    		: 0,
            "attack"		: 0,

            "arrow_vert_latch" : False,
            "arrow_hori_latch" : False,
            "left_click_latch" : False,
            "right_click_latch": False,
            "vertical_latch"   : False
        }
 
    def update(self):
        keys = pygame.key.get_pressed()

        # update player position based on key states
        if keys[pygame.K_a]:
           self.input_dict['horizontal'] = -1

        if keys[pygame.K_d]:
            self.input_dict['horizontal'] = 1
        
        if not keys[pygame.K_a] and not keys[pygame.K_d]:
            self.input_dict['horizontal'] = 0

        if keys[pygame.K_w]:
            self.input_dict["vertical"] = 1
        if keys[pygame.K_s]:
            self.input_dict['vertical'] = -1
        if not keys[pygame.K_w] and not keys[pygame.K_s]:
            self.input_dict['vertical'] = 0

        if keys[pygame.K_c] and not self.hold_create:
            self.input_dict['create-level'] = 1
            self.hold_create = True
        else:
            self.input_dict['create-level'] = 0

        if self.hold_create and not keys[pygame.K_c]:
            self.hold_create = False

        if keys[pygame.K_l]:
            self.input_dict["load-level"] = 1
        else:
            self.input_dict["load-level"] = 0

        if keys[pygame.K_UP]:
            self.input_dict["arrow-vert"] = 1
        elif keys[pygame.K_DOWN]:

            self.input_dict["arrow-vert"] = -1

        else:
            self.input_dict["arrow-vert"] = 0

        if keys[pygame.K_LEFT]:
            self.input_dict['arrow-hori'] = -1
        elif keys[pygame.K_RIGHT]:
            self.input_dict['arrow-hori'] = 1
        else:
            self.input_dict['arrow-hori'] = 0

        if keys[pygame.K_p]:
            self.input_dict["patch-level"] = 1
        else:
            self.input_dict["patch-level"] = 0

        if keys[pygame.K_LSHIFT]:
            self.input_dict["l-shift"] = 1
        else:
            self.input_dict["l-shift"] = 0

        if keys[pygame.K_e]:
            self.input_dict['edit'] = 1
        else:
            self.input_dict['edit'] = 0

        if keys[pygame.K_SPACE]:
            self.input_dict['attack'] = 1
        else:
            self.input_dict['attack'] = 0

        mouse_buttons = pygame.mouse.get_pressed()

        if mouse_buttons[0]:
            self.input_dict["left-click"] = 1
        else:
            self.input_dict["left-click"] = 0

        if mouse_buttons[2]:
            self.input_dict["right-click"] = 1
        else:
            self.input_dict["right-click"] = 0


        return self.input_dict
