import sys
sys.path.append('./Objects')
sys.path.append('./Objects/components')
import item_object
from vector import Vector
class SuperMushroom(item_object.ItemObject):
		def __init__(self):
			super().__init__()
			self.current_sprite.create_sprite('./GameData/Assets/Items/super_mushroom.png')
			self.physics.pause = False
			self.save_state.object_json_file='./GameData/jsons/super_mushroom.json'

			self.physics.direction.x = 1
			self.move_velocity = 100

		def update(self,**kwargs):
			self.move()

		def move(self):
			if self.collider.right:
				self.physics.direction.x = -1
			if self.collider.left:
				self.physics.direction.x = 1

			self.physics.initial_velocity.x = self.move_velocity*self.physics.direction.x


def create_object():
	return SuperMushroom()
