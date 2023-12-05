import sys

sys.path.append('./Objects')
sys.path.append('./Objects/components')
sys.path.append("./GameData/GameObjects")
import player_object
import enemy_object
from vector import Vector

class goomba(enemy_object.EnemyObject):
    def __init__(self):
        super().__init__()
        self.current_sprite.create_sprite('./GameData/Assets/Enemies/Goomba/goomba_32x32_idle.png')
        self.generic_sprite_1.create_sprite_sheet('./GameData/Assets/Enemies/Goomba/sprite_sheet/goomba_32x32_walk.png',
                                                  2, Vector(32, 32))
        self.generic_sprite_1.position = Vector(0, 0)
        self.generic_sprite_1.create_sprite_sheet_rect()
        self.generic_sprite_2.create_sprite('./GameData/Assets/Enemies/Goomba/states/goomba_32x32_death.png')
        self.physics.pause = False
        self.save_state.object_json_file = './GameData/jsons/goomba.json'
        self.animator.frame_count = 2
        self.animator.frame_duration = 200
        self.death_animation_triggered = False

        self.audio_dir = "./GameData/Assets/Audio/EnemyFX"
        self.audio.load_audio('stomp', self.audio_dir + "/smb_stomp.wav")

    def update(self, **kwargs):

        if not self.is_hit:
            self.generic_enemy_ai()
        if self.is_hit:
            self.physics.initial_velocity.x = 0
        self.animation()
        self.audio_handler()
        # self.damage_player()
        # self.handle_damage()

    def animation(self):
        self.animator.set_direction(self.physics)

        if abs(self.physics.initial_velocity.x) > 0 and not self.is_hit:
            self.animator.trigger_generic_animation(1)

        elif self.is_hit and not self.death_animation_triggered:
            self.animator.trigger_generic_animation(2)
            self.death_animation_triggered = True

        if self.death_animation_triggered and self.animator.determine_time_elapsed() > 1000:
            self.destroy = True

    def audio_handler(self):
        if self.death_animation_triggered and not self.audio.triggered['stomp']:
            self.audio.queue_audio('stomp')

    def handle_damage(self):
        if self.collider.up and isinstance(self.collider.up_collision_object, player_object.PlayerObject):
            self.is_hit = True

def create_object():
    return goomba()
