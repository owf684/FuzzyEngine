import sys
import math
sys.path.append('./Objects')
sys.path.append('./Objects/components')
import environment_object
import player_object

class BreakBrick(environment_object.EnvironmentObject):
		def __init__(self):
			super().__init__()
			self.current_sprite.create_sprite('./GameData/Assets/Environment/breakable_brick.png')
			self.physics.pause = True
			self.save_state.object_json_file='./GameData/jsons/break_brick.json'
			self.trigger_hit = False
			self.step = .1
			self.theta  = 1 
		def update(self):
			self.collisions()
			self.hit_animation()


		def collisions(self):
			if self.collider.down and isinstance(self.collider.down_collision_object,player_object.PlayerObject):
				if not self.trigger_hit:
					self.trigger_hit = True


		def hit_animation(self):

			if self.trigger_hit:
				self.physics.position.y += 2 * math.cos(self.theta * math.pi)
				self.theta -= self.step
				if self.theta <= 0:
					self.theta = 1
					self.trigger_hit = False

def create_object():
	return BreakBrick()
