import sys

sys.path.append("./Objects")
import scene_object


class CollisionEngine:

    def __init__(self):
        None

    def update(self, **kwargs):
        current_object = kwargs['CurrentObject']
        e_graphics = kwargs['GraphicsEngine']
        current_object.collider.reset()
        collision_buffer = None

        collision_buffer = self.get_collision_buffer(current_object, e_graphics)

        if collision_buffer is not None:
            for other in collision_buffer:
                self.detect_collisions(current_object, other)

    def detect_collisions(self, current_object, other):
        if (current_object != other
            and not isinstance(other, scene_object.SceneObject)
            and not isinstance(current_object, scene_object.SceneObject)) \
                and not current_object.collider.all_off:

            if current_object.current_sprite.rect.colliderect(other.current_sprite.rect) \
                    and not other.collider.pass_through:

                if not current_object.collider.up_off:
                    self.detect_up_collisions(current_object, other)

                if not current_object.collider.right_off:
                    self.detect_right_collisions(current_object, other)

                if not current_object.collider.down_off:
                    self.detect_down_collisions(current_object, other)

                if not current_object.collider.left_off:
                    self.detect_left_collisions(current_object, other)
    def get_collision_buffer(self, current_object, e_graphics):
        for i in range(e_graphics.resolution):
            if i * e_graphics.spacing - e_graphics.padding <= current_object.physics.position.x < (i + 1) * e_graphics.spacing + e_graphics.padding:
                return e_graphics.collision_buffer[i * e_graphics.spacing]
    def detect_up_collisions(self, current_object, other):
        if current_object.current_sprite.rect.top < other.current_sprite.rect.bottom \
                and current_object.current_sprite.rect.bottom > other.current_sprite.rect.bottom \
                and (
                other.current_sprite.rect.left < current_object.current_sprite.rect.centerx < other.current_sprite.rect.right \
                or other.current_sprite.rect.left < current_object.current_sprite.rect.left + 10 < other.current_sprite.rect.right \
                or other.current_sprite.rect.left < current_object.current_sprite.rect.right - 10 < other.current_sprite.rect.right):
            current_object.collider.up = True
            current_object.collider.up_collision_object = other

    def detect_right_collisions(self, current_object, other):
        if current_object.current_sprite.rect.right > other.current_sprite.rect.left \
                and current_object.current_sprite.rect.left < other.current_sprite.rect.left \
                and (
                other.current_sprite.rect.top < current_object.current_sprite.rect.centery < other.current_sprite.rect.bottom \
                or other.current_sprite.rect.top < current_object.current_sprite.rect.top + 10 < other.current_sprite.rect.bottom \
                or other.current_sprite.rect.top < current_object.current_sprite.rect.bottom - 10 < other.current_sprite.rect.bottom):
            current_object.collider.right = True
            current_object.collider.right_collision_object = other
            if current_object.physics.direction.x >= 0:
                current_object.physics.initial_position.x = other.current_sprite.rect.left - current_object.current_sprite.image.get_width() + 1

    def detect_down_collisions(self, current_object, other):
        if current_object.current_sprite.rect.bottom > other.current_sprite.rect.top \
                and current_object.current_sprite.rect.top < other.current_sprite.rect.top \
                and (
                other.current_sprite.rect.left < current_object.current_sprite.rect.centerx < other.current_sprite.rect.right \
                or other.current_sprite.rect.left < current_object.current_sprite.rect.right - 10 < other.current_sprite.rect.right \
                or other.current_sprite.rect.left < current_object.current_sprite.rect.left + 10 < other.current_sprite.rect.right):
            current_object.collider.down = True
            current_object.collider.down_collision_object = other
            if not current_object.collider.pass_through:
                current_object.physics.initial_position.y = other.current_sprite.rect.top - current_object.current_sprite.image.get_height() + 1

    def detect_left_collisions(self, current_object, other):
        if current_object.current_sprite.rect.left < other.current_sprite.rect.right \
                and current_object.current_sprite.rect.right > other.current_sprite.rect.right \
                and (
                other.current_sprite.rect.top < current_object.current_sprite.rect.centery < other.current_sprite.rect.bottom \
                or other.current_sprite.rect.top < current_object.current_sprite.rect.top + 10 < other.current_sprite.rect.bottom \
                or other.current_sprite.rect.top < current_object.current_sprite.rect.bottom - 10 < other.current_sprite.rect.bottom):
            current_object.collider.left = True
            current_object.collider.left_collision_object = other
            if current_object.physics.direction.x <= 0:
                current_object.physics.initial_position.x = other.current_sprite.rect.right
