from copy import deepcopy
from math import sqrt
class Vector:
  
  
  def __init__(self,x,y):
    self.x = x
    self.y = y
  
  def __add__(self,other):
    if isinstance(other, Vector):
      return Vector(self.x+other.x, self.y+other.y)
    else:
      raise TypeError("Unsupported operand type")

  def __sub__(self,other):
    if isinstance(other, Vector):
      return Vector(self.x-other.x, self.y-other.y)
    else:
      raise TypeError("Unsupported operand type")

  def __mul__(self,other):

    if isinstance(other,Vector): # return dot product
      return self.x*other.x + self.y*other.y
    elif isinstance(other,int) or isinstance(other,float): 
       return Vector(self.x*other, self.y*other)
    else:
      raise TypeError("Unsupported operand type")

  def __rmul__(self,other):
    if isinstance(other,Vector):
      return self.x*other.x + self.y*other.y
    elif isinstance(other,int) or isinstance(other,float):
      return Vector(self.x*other,self.y*other)
    else:
      raise TypeError("Unsupported operand type")    

  def __repr__(self):
    return ("Vector(" + str (self.x) + "," + str(self.y) + ")" )

  def __call__(self):
    return deepcopy(self)


  def magnitude(self):
    return sqrt( pow(self.x,2) + pow(self.y,2) )
