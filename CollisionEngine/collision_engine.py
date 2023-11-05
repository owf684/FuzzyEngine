

class CollisionEngine:


    def __init__(self):
        None



    def update(self,**kwargs):
        game_object = kwargs['CurrentObject']
        render_buffer = kwargs['RenderBuffer']
        game_object.collider.update(RenderBuffer=render_buffer,CurrentObject=game_object)