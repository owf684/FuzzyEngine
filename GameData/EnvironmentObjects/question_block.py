import sys
import math
sys.path.append('./Objects')
sys.path.append('./Objects/components')
sys.path.append('./GameData/GameObjects')
import player_object
from vector import Vector
import environment_object

class QuestionBlock(environment_object.EnvironmentObject):
		def __init__(self):
			super().__init__()
			self.current_sprite.create_sprite('./GameData/Assets/Environment/Question_block.png')
			self.physics.pause = True
			self.save_state.object_json_file='./GameData/jsons/question_block.json'
			self.generic_sprite_1.create_sprite_sheet('./GameData/Assets/Environment/question_block_states/question_block_sprite_sheet.png', 3, Vector(32, 32))
			self.generic_sprite_1.position = Vector(0, 0)
			self.generic_sprite_1.create_sprite_sheet_rect()
			self.generic_sprite_2.create_sprite('./GameData/Assets/Environment/question_block_states/question_block_hit.png')
			self.animator.frame_count = 3
			self.animator.frame_duration = 150
			self.question_block_state = 0
			self.step = .1
			self.theta  = 1 
			self.trigger_hit = False
		def update(self):
			self.animate()
			self.collisions()
			self.hit_animation()

		def animate(self):
			match self.question_block_state:

				case 0:
					self.animator.trigger_generic_animation(1)

				case 1:
					self.animator.trigger_generic_animation(2)

		def collisions(self):
			if self.collider.down and isinstance(self.collider.down_collision_object,player_object.PlayerObject):
				if self.question_block_state == 0:
					self.question_block_state = 1
					self.trigger_hit = True


		def hit_animation(self):

			if self.trigger_hit:
				self.physics.position.y += 2 * math.cos(self.theta * math.pi)
				self.theta -= self.step
				if self.theta <= 0:
					self.theta = 1
					self.trigger_hit = False
				

def create_object():
	return QuestionBlock()
