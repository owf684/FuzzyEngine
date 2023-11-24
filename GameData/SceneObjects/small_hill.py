import sys
sys.path.append('./Objects')
sys.path.append('./Objects/components')
import scene_object
class SmallHill(scene_object.SceneObject):
		def __init__(self):
			super().__init__()
			self.current_sprite.create_sprite('./GameData/Assets/Scenery/small_hill.png')
			self.physics.pause = True
			self.save_state.object_json_file='./GameData/jsons/small_hill.json'
def create_object():
	return SmallHill()
