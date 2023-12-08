from vector import Vector

class PhysicsComponent:


  def __init__(self):
    self.position = Vector(0,0)
    self.initial_position = Vector(0,0)
    self.displacement = Vector(0,0)
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
    self.gravity_force = 0
    self.pause_x_position = False


  def zero_speed(self,zero_x_components=False,zero_y_components=False):
    if zero_x_components:
      self.initial_velocity.x =0
      self.velocity.x = 0
      self.acceleration.x = 0    
      self.force.x = 0
      self.net_force.x = 0 

    if zero_y_components:
      self.initial_velocity.y=0
      self.velocity.y=0 
      self.acceleration.y=0
      self.force.y=0
      self.net_force.y=0


    