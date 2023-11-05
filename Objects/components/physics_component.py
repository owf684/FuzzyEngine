from vector import Vector

class PhysicsComponent:


  def __init__(self):
    self.position = Vector(0,0)
    self.initial_position = Vector(0,0)
    self.velocity = Vector(0,0)
    self.initial_velocity = Vector(0,0)
    self.acceleration = Vector(0,0)
    self.force = Vector(0,0)
    self.net_force = Vector(0,0)
    self.k = Vector(1,0) 
    self.direction = Vector(0,0)
    self.friction = Vector(0,0)
    self.momentum = Vector(0,0)
    self.mass = 100
    self.energy = 0
    self.pause = False
    self.gravity = 0

  def calculate_force(self,gravity):
    '''
    F = m * a ==> a = F / m
    '''	

    if self.mass != 0:

      # calculate damping force x
      damping_force = self.k.x * self.velocity.x

      # calculate net force x on object
      self.net_force.x = self.force.x - damping_force
   	 
      # calculate x acceleration
      self.acceleration.x = self.net_force.x / self.mass

      # calculate damping force y
      damping_force = self.k.y * self.velocity.y

      # calculate force due to gravity
      gravity_force = self.mass*gravity

      # calculate net force y on object
      self.net_force.y = -self.force.y - gravity_force - damping_force

      print(self.force.y)
      print(gravity_force)
      print(self.net_force.y)
      # calculate accleration y
      self.acceleration.y = self.net_force.y / self.mass

 

  def calculate_velocity(self,delta_t):
      
    # update velocity x
    self.velocity.x = self.initial_velocity.x + self.acceleration.x * delta_t

    # update velocity y 
    self.velocity.y = self.initial_velocity.y + self.acceleration.y * delta_t

    # update initial velocity  
    self.initial_velocity = self.velocity() 
 

  def calculate_position(self,delta_t):

    ''' 
    Kinematic Equations
    x = x_initial + v_x_initial * t + 0.5 *a * t ^ 2
    y = y_initial + v_y_initial * t + 0.5 *a * t ^ 2
    '''
   
    # calculate x position
    self.position.x = self.initial_position.x + ( self.initial_velocity.x * delta_t ) +  ( 0.5 * self.acceleration.x * pow(delta_t,2) )

    # calculate y position
    self.position.y = self.initial_position.y + ( self.initial_velocity.y * delta_t ) +  ( 0.5 * self.acceleration.y * pow(delta_t,2) ) 

    # update initial position
    self.initial_position = self.position()    


  def update(self,gravity=9.8,delta_t=0.0133):
    self.calculate_force(gravity)
    self.calculate_velocity(delta_t)
    self.calculate_position(delta_t)      
