import sys
sys.path.append("./Objects")
import item_object 


class ItemEngine:


    def __init__(self):
        None


    def update(self,**kwargs):

        objects = kwargs['GameObject']

        if isinstance(objects,item_object.ItemObject):
            objects.update()