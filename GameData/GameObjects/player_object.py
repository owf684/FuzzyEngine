import sys

sys.path.append('./Objects')
sys.path.append('./Objects/components')
import game_object
import enemy_object
from vector import Vector


class PlayerObject(game_object.GameObject):

    def __init__(self):
        super().__init__()

        self.current_sprite.create_sprite('./GameData/Assets/PlayerSprites/mario/mario_idle_right.png')
        self.generic_sprite_1.create_sprite_sheet('./GameData/Assets/PlayerSprites/mario/mario_run_right.png', 3,
                                                  Vector(32, 32))
        self.generic_sprite_1.position = Vector(0, 0)
        self.generic_sprite_1.create_sprite_sheet_rect()
        self.generic_sprite_2.create_sprite('./GameData/Assets/PlayerSprites/mario/mario_idle_right.png')
        self.generic_sprite_3.create_sprite('./GameData/Assets/PlayerSprites/mario/mario_jump_right.png')
        self.generic_sprite_4.create_sprite('./GameData/Assets/PlayerSprites/mario/mario_death.png')

        self.animator.frame_count = 3
        self.animator.frame_duration = 120

        self.save_state.object_json_file = './GameData/jsons/player_object.json'  # needed for creating scenes.
        # setup some variables
        self.physics.k.x = 400
        self.physics.k.y = 0

        # other vairables
        self.is_hit = False

        self.player_walking_force = 60000

        self.player_running_force = 120000

        self.initial_jump_velocity = -200

        self.jump_velocity_increment = 2000

        self.max_jump_velocity = -375

        self.hit_handled = False

        self.cap_jump_velocity = False

        self.jumping = False

        self.audio_dir = "./GameData/Assets/Audio"

        self.audio.load_audio('small-jump', self.audio_dir + "/MarioFX/smb_jump-small.wav")

    def update(self, **kwargs):
        # get relevant variables
        input_dict = kwargs['InputDict']
        delta_t = kwargs['DeltaT']

        # update object
        if not self.is_hit:
            self.x_movement(input_dict)
            self.y_movement(input_dict, delta_t)
            self.damage_enemy()

        self.animation_handler(input_dict)
        self.audio_handler()
        self.damage_handler()

    def x_movement(self, input_dict):
        self.physics.direction.x = input_dict['horizontal']
        if input_dict['l-shift']:
            self.animator.frame_duration = 60
            self.physics.force.x = self.player_running_force * self.physics.direction.x
        else:
            self.animator.frame_duration = 120
            self.physics.force.x = self.player_walking_force * self.physics.direction.x

    def y_movement(self, input_dict, delta_t):
        if input_dict['vertical'] == 1 and not input_dict['vertical_latch'] and self.collider.down:

            self.physics.direction.y = input_dict['vertical']
            self.physics.initial_velocity.y = self.initial_jump_velocity
            input_dict['vertical_latch'] = True

        elif input_dict['vertical'] == 1 and input_dict[
            'vertical_latch'] and not self.collider.down and not self.cap_jump_velocity:

            self.physics.initial_velocity.y -= self.jump_velocity_increment * delta_t
            if (self.physics.initial_velocity.y <= self.max_jump_velocity) or self.collider.up:
                self.cap_jump_velocity = True

        elif input_dict['vertical'] == 0 and input_dict['vertical_latch']:

            input_dict['vertical_latch'] = False
            self.physics.direction.y = input_dict['vertical']
            self.cap_jump_velocity = False

    def animation_handler(self, input_dict):
        # update direction
        self.animator.set_direction(self.physics)

        # reset jump animation
        if self.jumping and self.collider.down:
            self.jumping = False

        if not self.jumping and not self.is_hit:

            # walk animation
            if abs(input_dict['horizontal']) > 0:
                self.animator.trigger_generic_animation(1)

            # idle animation
            elif input_dict['horizontal'] == 0:
                self.animator.trigger_generic_animation(2)

            # set jump flag
            if input_dict['vertical'] == 1 and self.collider.down:
                self.jumping = True

        # jump animation
        if self.jumping and not self.collider.down and not self.is_hit:
            self.animator.trigger_generic_animation(3)

        if self.is_hit:
            self.animator.trigger_generic_animation(4)

    def audio_handler(self):

        # jump audio
        if self.jumping and self.collider.down and not self.audio.triggered['small-jump']:
            self.audio.queue_audio('small-jump')

        if not self.jumping and self.collider.down:
            self.audio.triggered['small-jump'] = False

    def damage_enemy(self):

        if self.collider.down and isinstance(self.collider.down_collision_object, enemy_object.EnemyObject) \
            and not self.collider.down_collision_object.is_hit:
            self.collider.down_collision_object.is_hit = True
            self.collider.down_collision_object.collider.pass_through = True
            self.collider.down_collision_object.collider.left_off = True
            self.collider.down_collision_object.collider.right_off = True
            self.collider.down_collision_object.collider.up_off = True
            self.physics.initial_velocity.y = -200

    def damage_handler(self):
        if isinstance(self.collider.left_collision_object,enemy_object.EnemyObject) \
                and not self.collider.left_collision_object.is_hit:
            if self.collider.left:
                self.is_hit = True

        if isinstance(self.collider.right_collision_object,enemy_object.EnemyObject) \
                and not self.collider.right_collision_object.is_hit:
            if self.collider.right:
                self.is_hit = True

        if self.is_hit and not self.hit_handled:
            self.collider.all_off = True
            self.hit_handled = True
            self.physics.zero_speed(True,False)
            self.physics.initial_velocity.y = -500

def create_object():
    return PlayerObject()
