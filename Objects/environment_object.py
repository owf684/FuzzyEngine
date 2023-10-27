import sys
sys.path.append("./Objects/components")
import sprite_component
import physics_component

class GameObject:

    def __init__(self):
        self.current_sprite   = sprite_component.SpriteComponent()
        self.generic_sprite_1 = sprite_component.SpriteComponent()
        self.generic_sprite_2 = sprite_component.SpriteComponent()
        self.generic_sprite_3 = sprite_component.SpriteComponent()
        self.generic_sprite_4 = sprite_component.SpriteComponent()

        self.physics = physics_component.PhysicsComponent()
        