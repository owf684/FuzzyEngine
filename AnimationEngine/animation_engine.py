import pygame

class AnimationEngine:

    def __init__(self):

        None

    def update(self,**kwargs):

        objects = kwargs['GameObject']
        
        match objects.animator.which_sheet:

            case 1:
                self.set_current_sprite(objects,objects.generic_sprite_1)
            case 2:
                self.set_current_sprite(objects,objects.generic_sprite_2)
            case 3:
                self.set_current_sprite(objects,objects.generic_sprite_3)
            case 4:
                self.set_current_sprite(objects,objects.generic_sprite_4)


    def set_current_sprite(self,objects,generic_sprite):
        try:

            if len(generic_sprite.sprite_sheet) > 0:

                objects.animator.determine_frame_count()
        
                if objects.animator.direction_x == -1:
                    objects.current_sprite.image = pygame.transform.flip(generic_sprite.sprite_sheet[objects.animator.frame_index],True,False)
                else:
                    objects.current_sprite.image = generic_sprite.sprite_sheet[objects.animator.frame_index]
            elif generic_sprite.image is not None:
                if objects.animator.direction_x == -1:
                    objects.current_sprite.image = pygame.transform.flip(generic_sprite.image,True,False)
                else:
                    objects.current_sprite.image = generic_sprite.image
            
        except Exception as Error:
            print(objects.animator.which_sheet)


