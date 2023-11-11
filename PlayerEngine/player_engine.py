import pygame


class PlayerEngine:

    def __init__(self):
        None
    def update(self,**kwargs):
        player_object = kwargs['PlayerObject']
        delta_t=kwargs['DeltaT']
        player_object.update(InputDict=kwargs['InputDict'],DeltaT=delta_t)
    