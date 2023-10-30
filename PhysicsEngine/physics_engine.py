
class PhysicsEngine:


    def __init__(self):
        self.gravity = -9.8*10



    def update(self,**kwargs):
        game_object = kwargs['GameObject']
        delta_t = kwargs['DeltaT']
        
        if not game_object.physics.pause:
            game_object.physics.update(gravity=self.gravity,delta_t=delta_t)
