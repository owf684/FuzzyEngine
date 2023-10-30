

class SpriteEngine:

    def __init__(self):
        None


    def update(self,**kwargs):
        game_object = kwargs['GameObject']

        game_object.current_sprite.update(game_object.physics.position)