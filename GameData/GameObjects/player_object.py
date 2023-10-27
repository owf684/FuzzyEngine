import sys
sys.path.append('./Objects')
sys.path.append('./Objects/components')
import game_object

class PlayerObject(game_object.GameObject):

    def __init__(self):
        super().__init__()

        self.current_sprite.create_sprite('./GameData/Assets/PlayerSprites/chris.png')
        self.generic_sprite_1.create_sprite('./GameData/Assets/PlayerSprites/chris.png')

        #setup some variables
        self.physics.k.x = 100
        self.physics.k.y = 0
    




def create_object():
    return PlayerObject()