import sys
sys.path.append("./Objects")
import environment_object

class EnvironmentEngine:


    def __init__(self):

        None


    def update(self,**kwargs):

        objects = kwargs['GameObject']

        if isinstance(objects,environment_object.EnvironmentObject):
            objects.update()