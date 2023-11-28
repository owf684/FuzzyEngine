import pygame
class AnimationComponent:

    def __init__(self):
        try:
            self.elapsed_time = 0
            self.current_time = 0
            self.last_frame_time = 0

            self.frame_index = 0
            self.frame_duration = 0
            self.frame_count = 0
    
            self.timer_started = False

            self.current_time_2 = 0
            self.elapsed_time_2 = 0
            self.last_frame_time_2 = 0
            self.which_sheet = 0
            self.direction_x = 0
        except Exception as Error:
            print("ERROR::anim_util.py::__init__()", Error)
            
    def determine_frame_count(self):
        try:
             
            self.current_time = pygame.time.get_ticks()
            self.elapsed_time = self.current_time - self.last_frame_time

            if self.elapsed_time >= self.frame_duration:
                self.frame_index = (self.frame_index + 1) % self.frame_count
                self.last_frame_time = self.current_time

        except Exception as Error:
            print("ERROR::anim_util.py::determine_frame_count", Error)
            
   
    def determine_time_elapsed(self):
        try:

            self.current_time_2 = pygame.time.get_ticks()
            self.elapsed_time_2 = self.current_time_2 - self.last_frame_time_2
            return self.elapsed_time_2
        except Exception as Error:
            print("ERROR::anim_util.py::determine_time_elapsed", Error)

    def reset_time_variables(self):
        try:

            self.elapsed_time_2 = 0
            self.current_time_2 = 0
            self.last_frame_time_2 = 0
            self.frame_index = 0
        except Exception as Error:
            print("ERROR::anim_util.py::reset_time_variables", Error)

    def trigger_generic_animation(self, i_generic_sprite):
        # ensure only acceptable parameters are input
        if i_generic_sprite > 4:
            self.which_sheet = 4
        elif i_generic_sprite < 0:
            self.which_sheet = 0
        else:
            self.which_sheet = i_generic_sprite

    def set_direction(self,physics):
        if abs(physics.direction.x) > 0:
            self.direction_x = physics.direction.x