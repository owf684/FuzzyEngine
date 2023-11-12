
class PhysicsEngine:


    def __init__(self):
        self.gravity = -9.8*50



    def update(self,**kwargs):
        game_object = kwargs['GameObject']
        delta_t = kwargs['DeltaT']
        if not game_object.physics.pause:
            self.calculate_force(game_object)
            self.calculate_velocity(game_object,delta_t)
            self.calculate_position(game_object,delta_t)             
 
 
    def calculate_force(self,game_object):
        '''
        F = m * a ==> a = F / m
        '''	

        if game_object.physics.mass != 0:

        # adjust gravitational force collisions
            if game_object.collider.down:
                gravity = 0
            else:
                gravity = self.gravity

        # calculate damping force x
            damping_force = game_object.physics.k.x * game_object.physics.velocity.x

        # calculate net force x on object
            game_object.physics.net_force.x = game_object.physics.force.x - damping_force
   	 
        # calculate x acceleration
            game_object.physics.acceleration.x = game_object.physics.net_force.x / game_object.physics.mass

        # calculate damping force y
            damping_force = game_object.physics.k.y * game_object.physics.velocity.y

         # calculate force due to gravity
            gravity_force = game_object.physics.mass*gravity
            game_object.physics.gravity_force = gravity_force

        # calculate net force y on object
            game_object.physics.net_force.y = int(-game_object.physics.force.y - gravity_force - damping_force)

        # calculate accleration y
            game_object.physics.acceleration.y = game_object.physics.net_force.y / game_object.physics.mass

 

    def calculate_velocity(self,game_object,delta_t):
      
    # update velocity x
        game_object.physics.velocity.x = game_object.physics.initial_velocity.x + game_object.physics.acceleration.x * delta_t

    # update velocity y 
        game_object.physics.velocity.y = game_object.physics.initial_velocity.y + game_object.physics.acceleration.y * delta_t

    # update initial velocity  
        game_object.physics.initial_velocity = game_object.physics.velocity() 
 
    # adjust velocity for collisions 
        if game_object.collider.up:
            game_object.physics.initial_velocity.y = 100
        if game_object.collider.down and game_object.physics.direction.y != 1:
            game_object.physics.initial_velocity.y = 0
            game_object.physics.velocity.y = 0
            game_object.physics.net_force.y =0
        if game_object.collider.right:
            game_object.physics.initial_velocity.x = 0
            game_object.physics.net_force.x = 0
        if game_object.collider.left:
            game_object.physics.initial_velocity.x = 0
            game_object.physics.net_force.x = 0


    def calculate_position(self, game_object,delta_t):

        ''' 
        Kinematic Equations
        x = x_initial + v_x_initial * t + 0.5 *a * t ^ 2
        y = y_initial + v_y_initial * t + 0.5 *a * t ^ 2
        '''
   
        # calculate x position
        game_object.physics.position.x = game_object.physics.initial_position.x + ( game_object.physics.initial_velocity.x * delta_t ) +  ( 0.5 * game_object.physics.acceleration.x * pow(delta_t,2) )

        # calculate y position
        game_object.physics.position.y = game_object.physics.initial_position.y + ( game_object.physics.initial_velocity.y * delta_t ) +  ( 0.5 * game_object.physics.acceleration.y * pow(delta_t,2) ) 

        # update initial position
        game_object.physics.initial_position = game_object.physics.position()    


   
