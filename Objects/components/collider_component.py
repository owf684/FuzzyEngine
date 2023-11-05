

class ColliderComponent:

    def __init__(self):

        self.collisions = {
            "up": False,
            "right": False,
            "down": False,
            "left": False
        }


    
    def update(self,**kwargs):

        render_buffer = kwargs['RenderBuffer']
        current_object = kwargs['CurrentObject']
        for objects in render_buffer:
            if objects != current_object:
                 
                self.detect_up_collision(current_object,objects)
                self.detect_right_collision(current_object,objects)
                self.detect_down_collision(current_object,objects)
                self.detect_left_collision(current_object,objects)
                self.on_collision_down(current_object,objects)
    def detect_up_collision(self,current_object,objects):
        None
    def detect_right_collision(self,current_object,objects):
        None
    def detect_down_collision(self,current_object,objects):
        if current_object.current_sprite.rect.bottom > objects.current_sprite.rect.top:
            if current_object.current_sprite.rect.top < objects.current_sprite.rect.top:
                 
                if current_object.current_sprite.rect.colliderect(objects.current_sprite.rect):
                    self.collisions['down'] = True
        else:
            self.collisions['down'] = False

    def detect_left_collision(self, current_object, objects):
        None

    def on_collision_down(self,current_object, objects):
        if self.collisions['down']:
    
            current_object.physics.force.y = 1*current_object.physics.mass*9.8*10
            current_object.physics.velocity.y = 0
            current_object.physics.initial_velocity.y = 0
    
