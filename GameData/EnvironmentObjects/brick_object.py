import sys
sys.path.append('./Objects')
sys.path.append('./Objects/components')
import game_object

class BrickObject(game_object.GameObject):

    def __init__(self):
        super().__init__()

        self.current_sprite.create_sprite('./GameData/Assets/Environment/brick.png')



def create_object():
    return BrickObject()