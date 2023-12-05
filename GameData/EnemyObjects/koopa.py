import sys
sys.path.append('./Objects')
sys.path.append('./Objects/components')
sys.path.append('./GameData/GameObjects')
import enemy_object
import player_object
from vector import Vector
class koopa(enemy_object.EnemyObject):
		def __init__(self):
			super().__init__()
			self.current_sprite.create_sprite('./GameData/Assets/Enemies/KoopaTroopa/KoopaTroopa_idle.png')
			self.generic_sprite_1.create_sprite_sheet('./GameData/Assets/Enemies/KoopaTroopa/sprite_sheet/KoopaTroopa_walkiing_left.png', 2 , Vector(32, 48))
			self.generic_sprite_1.position = Vector(0,0)
			self.generic_sprite_1.create_sprite_sheet_rect()
			self.generic_sprite_2.create_sprite_sheet('./GameData/Assets/Enemies/KoopaTroopa/states/KoopaShell_revive.png', 2, Vector(32, 48))
			self.generic_sprite_2.position = Vector(0,0)
			self.generic_sprite_2.create_sprite_sheet_rect()
			self.generic_sprite_3.create_sprite('./GameData/Assets/Enemies/KoopaTroopa/states/KoopaShell.png')
			self.physics.pause = False
			self.animator.frame_count = 2
			self.animator.frame_duration = 150
			self.save_state.object_json_file='./GameData/jsons/koopa.json'
			self.death_animation_triggered = False
			self.revive_animation_triggered = False
			self.sliding_animation_triggered = False

			self.sliding = False
			self.sliding_direction = 0

		def update(self):
			if not self.is_hit and not self.sliding:
				self.generic_enemy_ai()
			if self.sliding:
				self.slide()

			self.animate()
			self.handle_damage()
		def animate(self):
			self.animator.set_direction(self.physics)
			if abs(self.physics.velocity.x) > 0 and not self.is_hit and not self.sliding:
				self.animator.trigger_generic_animation(1)

			if self.is_hit and not self.death_animation_triggered:
				self.animator.trigger_generic_animation(3)
				self.death_animation_triggered = True
				self.collider.pass_through = False
				self.collider.left_off = False
				self.collider.right_off = False
				self.collider.up_off = False

			if self.death_animation_triggered and not self.revive_animation_triggered and self.animator.determine_time_elapsed() > 3000:
				self.animator.trigger_generic_animation(2)
				self.animator.frame_duration = 200
				self.revive_animation_triggered = True

			if self.revive_animation_triggered and self.animator.determine_time_elapsed() > 1500:
				self.revive_animation_triggered = False
				self.death_animation_triggered = False
				self.is_hit = False

			if self.death_animation_triggered or self.revive_animation_triggered:
				if self.collider.left and isinstance(self.collider.left_collision_object,player_object.PlayerObject):
					self.sliding = True
					self.sliding_direction = 1
				if self.collider.right and isinstance(self.collider.right_collision_object,player_object.PlayerObject):
					self.sliding = True
					self.sliding_direction = -1

			if self.sliding and not self.sliding_animation_triggered:
				self.death_animation_triggered = False
				self.revive_animation_triggered = False
				self.sliding_animation_triggered = True
				self.animator.trigger_generic_animation(3)

			if self.sliding_animation_triggered and self.animator.determine_time_elapsed() > 100:
				self.is_hit = False

		def handle_damage(self):
			if self.is_hit:
				self.physics.initial_velocity.x = 0

		def slide(self):
			self.physics.initial_velocity.x = 350*self.sliding_direction
			if self.collider.right:
				self.sliding_direction = -1

			if self.collider.left:
				self.sliding_direction = 1

def create_object():
	return koopa()
