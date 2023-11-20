import sys
sys.path.append('./Objects')
sys.path.append('./Objects/components')
import environment_object
class BreakBrick(environment_object.EnvironmentObject):
		def __init__(self):
			super().__init__()
			self.current_sprite.create_sprite('./GameData/Assets/Environment/breakable_brick.png')
			self.physics.pause = True
			self.save_state.object_json_file='./GameData/jsons/break_brick.json'
def create_object():
	return BreakBrick()
