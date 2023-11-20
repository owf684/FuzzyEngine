import sys
sys.path.append('./Objects')
sys.path.append('./Objects/components')
import game_object
class FailedModuleLoad(game_object.GameObject):
		def __init__(self):
			super().__init__()
			self.current_sprite.create_sprite('./LevelEditor/components/FailedModuleLoad/donut.png')
			self.physics.pause = True
			self.save_state.object_json_file='./LevelEditor/components/FailedModuleLoad/donut.json'
def create_object():
	return FailedModuleLoad()
