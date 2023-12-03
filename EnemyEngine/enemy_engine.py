import pygame
import sys
sys.path.append("./Objects")
import enemy_object

class EnemyEngine:


    def update(self,**kwargs):
        objects= kwargs['GameObject']
        e_scroll = kwargs['ScrollEngine']

        if isinstance(objects,enemy_object.EnemyObject):
            objects.update()

    