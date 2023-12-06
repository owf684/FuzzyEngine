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
        self.generic_sprite_3.create_sprite('./GameData/Assets/Enemies/Goomba/states/goomba_32x32_death_ud.png')

        self.physics.pause = False
        self.save_state.object_json_file = './GameData/jsons/goomba.json'
        self.animator.frame_count = 2
        self.animator.frame_duration = 200
        self.death_animation_triggered = False
        self.goomba_state = 0
        self.audio_dir = "./GameData/Assets/Audio/EnemyFX"
        self.audio.load_audio('stomp', self.audio_dir + "/smb_stomp.wav")

    def update(self, **kwargs):

        if not self.is_hit:
            self.generic_enemy_ai()
        if self.is_hit:
            self.physics.initial_velocity.x = 0
        self.animation()
        self.audio_handler()
        self.handle_damage()

    def animation(self):
        self.animator.set_direction(self.physics)

        match self.goomba_state:
            case 0: # walk animation
                if abs(self.physics.initial_velocity.x) > 0:
                    self.animator.trigger_generic_animation(1)

            case 1:  # squashed
                self.animator.trigger_generic_animation(2)
                self.goomba_state = 2

            case 2:  # wait before destroying
                if self.animator.determine_time_elapsed() > 1000:
                    self.destroy = True     

            case 3:   # trigger death animation
                self.animator.trigger_generic_animation(3)
                self.goomba_state = 4

            case 4:  # wait before destorying
                if self.animator.determine_time_elapsed() > 2000:
                    #self.destroy = True
                    None
                
 
    def audio_handler(self):
        if (self.goomba_state == 1 or self.goomba_state ==3) and not self.audio.triggered['stomp']:
            self.audio.queue_audio('stomp')

    def handle_damage(self):
     
        if self.is_hit and self.goomba_state == 0:
            self.goomba_state = 1

        if self.attack_by_enemy and self.goomba_state <= 2:
            self.goomba_state = 3
            self.physics.direction.y = 1
            self.physics.initial_velocity.y = -300
            self.collider.all_off = True
            self.is_hit = True

def create_object():
    return goomba()
