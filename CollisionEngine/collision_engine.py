

class CollisionEngine:


    def __init__(self):
        None

    def update(self,**kwargs):
        current_object = kwargs['CurrentObject']
        render_buffer = kwargs['RenderBuffer']
        current_object.collider.reset()
        for other in render_buffer:
            if current_object != other:
                if current_object.current_sprite.rect.colliderect(other.current_sprite.rect):

                    self.detect_right_collisions(current_object,other)
                    self.detect_down_collisions(current_object,other)
                    self.detect_left_collisions(current_object,other)

    def detect_down_collisions(self,current_object,other):
        if current_object.current_sprite.rect.bottom > other.current_sprite.rect.top \
            and current_object.current_sprite.rect.top < other.current_sprite.rect.top \
            and other.current_sprite.rect.left < current_object.current_sprite.rect.centerx < other.current_sprite.rect.right:
            current_object.collider.down = True                
            current_object.physics.initial_position.y = other.current_sprite.rect.top-current_object.current_sprite.image.get_height() + 1
        
    def detect_right_collisions(self,current_object,other):
        if current_object.current_sprite.rect.right > other.current_sprite.rect.left \
            and current_object.current_sprite.rect.left < other.current_sprite.rect.left \
            and other.current_sprite.rect.top < current_object.current_sprite.rect.centery < other.current_sprite.rect.bottom:
            current_object.collider.right = True
            current_object.physics.initial_position.x = other.current_sprite.rect.left-current_object.current_sprite.image.get_width()+1
    
    def detect_left_collisions(self,current_object,other):
        if current_object.current_sprite.rect.left < other.current_sprite.rect.right \
            and current_object.current_sprite.rect.right > other.current_sprite.rect.right \
            and other.current_sprite.rect.top < current_object.current_sprite.rect.centery < other.current_sprite.rect.bottom:
                current_object.collider.left = True
                current_object.physics.initial_position.x = other.current_sprite.rect.right
            