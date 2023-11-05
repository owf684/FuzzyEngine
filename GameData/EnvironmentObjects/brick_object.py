import sys
sys.path.append('./Objects')
sys.path.append('./Objects/components')
import environment_object

class BrickObject(environment_object.EnvironmentObject):

    def __init__(self):
        super().__init__()

        self.current_sprite.create_sprite('./GameData/Assets/Environment/brick.png')

        self.physics.pause = True

def create_object():
    return BrickObject()