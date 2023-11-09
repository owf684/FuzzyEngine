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
    self.gravity_force = 0

