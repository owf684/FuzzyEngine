import pygame
import sys
sys.path.append('./GameData/GameObjects')
import player_object

class PlayerEngine:

    def __init__(self):
        None
    def update(self,**kwargs):
        o_player = kwargs['PlayerObject']
        delta_t=kwargs['DeltaT']
        if isinstance(o_player,player_object.PlayerObject):
            o_player.update(InputDict=kwargs['InputDict'],DeltaT=delta_t)
    