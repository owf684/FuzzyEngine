import sys

sys.path.append("./Objects/components")
import sprite_component
import physics_component
import collider_component
import save_component
import animation_component
import audio_component


class EnemyObject:

    def __init__(self):
        # sprites
        self.current_sprite = sprite_component.SpriteComponent()
        self.generic_sprite_1 = sprite_component.SpriteComponent()
        self.generic_sprite_2 = sprite_component.SpriteComponent()
        self.generic_sprite_3 = sprite_component.SpriteComponent()
        self.generic_sprite_4 = sprite_component.SpriteComponent()

        # physics
        self.physics = physics_component.PhysicsComponent()

        # collider
        self.collider = collider_component.ColliderComponent()

        # save state
        self.save_state = save_component.SaveComponent()

        # animation component
        self.animator = animation_component.AnimationComponent()

        # audio component
        self.audio = audio_component.AudioComponent()


        # enemy specific initializers
        self.physics.direction.x = 1
        self.walking_force = 50


    def generic_enemy_ai(self):
        
        self.physics.initial_velocity.x =self.walking_force*self.physics.direction.x

        if self.physics.direction.x == 1 and self.collider.right:
            self.physics.direction.x = -1

        if self.physics.direction.x == -1 and self.collider.left:
            self.physics.direction.x = 1


