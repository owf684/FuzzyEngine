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
        self.generic_sprite_1.create_sprite_sheet(
            './GameData/Assets/Enemies/KoopaTroopa/sprite_sheet/KoopaTroopa_walkiing_left.png', 2, Vector(32, 48))
        self.generic_sprite_1.position = Vector(0, 0)
        self.generic_sprite_1.create_sprite_sheet_rect(y_height_offset=10)
        self.generic_sprite_2.create_sprite_sheet('./GameData/Assets/Enemies/KoopaTroopa/states/KoopaShell_revive.png',
                                                  2, Vector(32, 48))
        self.generic_sprite_2.position = Vector(0, 0)
        self.generic_sprite_2.create_sprite_sheet_rect(y_height_offset=10)
        self.generic_sprite_3.create_sprite('./GameData/Assets/Enemies/KoopaTroopa/states/KoopaShell.png')
        self.physics.pause = False
        self.animator.frame_count = 2
        self.animator.frame_duration = 150
        self.save_state.object_json_file = './GameData/jsons/koopa.json'
        self.death_animation_triggered = False
        self.revive_animation_triggered = False
        self.sliding_animation_triggered = False
        self.koopa_state = 0  # 0 is active, 1 is hit, 2 is reviving, 3 is sliding
        self.sliding = False
        self.sliding_direction = 0

    def update(self):
        if self.koopa_state == 0:
            self.generic_enemy_ai()

        self.animate()
        self.handle_damage()
        self.slide()
        self.damage_enemy()
    def animate(self):
        self.animator.set_direction(self.physics)
        match self.koopa_state:
            case 0:  # active
                self.animator.trigger_generic_animation(1)

            case 1:  # hit
                self.animator.trigger_generic_animation(3)
                self.collider.pass_through = False
                self.collider.left_off = False
                self.collider.right_off = False
                self.collider.up_off = False
                self.koopa_state = 2

            case 2:  # waiting for timer to transition hit to revive
                if self.animator.determine_time_elapsed() > 3000:
                    self.animator.trigger_generic_animation(2)
                    self.animator.frame_duration = 200
                    self.koopa_state = 3

            case 3:
                if self.animator.determine_time_elapsed() > 1500:
                    self.is_hit = False
                    self.koopa_state = 0

            case 4:
                self.animator.trigger_generic_animation(3)
                self.koopa_state = 5
            case 5:
                if self.animator.determine_time_elapsed() > 500:
                    self.is_hit = False
            
    def handle_damage(self):
        if self.is_hit:
            self.physics.initial_velocity.x = 0
            if self.koopa_state == 0:
                self.koopa_state = 1

    def slide(self):
        if 1 <= self.koopa_state <= 3:
            if self.collider.left and isinstance(self.collider.left_collision_object, player_object.PlayerObject):
                self.koopa_state = 4
            if self.collider.right and isinstance(self.collider.right_collision_object, player_object.PlayerObject):
                self.koopa_state = 4
            if self.koopa_state == 4:
                self.sliding = True

        if self.sliding:

            self.physics.initial_velocity.x = 350 * self.physics.direction.x
            if self.collider.right and not isinstance(self.collider.right_collision_object,enemy_object.EnemyObject):
                self.physics.direction.x = -1
            if self.collider.left and not isinstance(self.collider.left_collision_object, enemy_object.EnemyObject):
                self.physics.direction.x = 1

    def damage_enemy(self):
        if self.sliding:
            if self.collider.left and isinstance(self.collider.left_collision_object,enemy_object.EnemyObject):
                self.collider.left_collision_object.attack_by_enemy = True
            if self.collider.right and isinstance(self.collider.right_collision_object,enemy_object.EnemyObject):
                self.collider.right_collision_object.attack_by_enemy = True

def create_object():
    return koopa()
