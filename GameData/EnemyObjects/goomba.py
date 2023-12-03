import sys
sys.path.append('./Objects')
sys.path.append('./Objects/components')
import enemy_object
from vector import Vector
class goomba(enemy_object.EnemyObject):
		def __init__(self):
			super().__init__()
			self.current_sprite.create_sprite('./GameData/Assets/Enemies/Goomba/goomba_32x32_idle.png')
			self.generic_sprite_1.create_sprite_sheet('./GameData/Assets/Enemies/Goomba/sprite_sheet/goomba_32x32_walk.png' , 2,Vector(32,32))
			self.generic_sprite_1.position = Vector(0,0)
			self.generic_sprite_1.create_sprite_sheet_rect()
			self.generic_sprite_2.create_sprite('./GameData/Assets/Enemies/Goomba/states/goomba_32x32_death.png')
			self.physics.pause =False
			self.save_state.object_json_file='./GameData/jsons/goomba.json'
			self.animator.frame_count = 2
			self.animator.frame_duration = 200
		def update(self,**kwargs):
			self.generic_enemy_ai()
			self.animation()

		def animation(self):
			self.animator.set_direction(self.physics)

			if abs(self.physics.initial_velocity.x) > 0:
				self.animator.trigger_generic_animation(1)
			
def create_object():
	return goomba()
