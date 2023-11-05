import pygame


class PlayerEngine:

    def __init__(self):
        self.player_walking_force = 20000
        self.thrust_force = -100000
    def update(self,**kwargs):
        player_object = kwargs['PlayerObject']
        input_dict = kwargs['InputDict']
        self.x_movement(player_object,input_dict)
        #self.y_movement(player_object,input_dict)



    def x_movement(self,player_object,input_dict):
        player_object.physics.direction.x = input_dict['horizontal']
        player_object.physics.force.x = self.player_walking_force*player_object.physics.direction.x

    def y_movement(self,player_object,input_dict):
        player_object.physics.direction.y = input_dict['vertical']
        player_object.physics.initial_velocity.y = self.thrust_force*player_object.physics.direction.y
