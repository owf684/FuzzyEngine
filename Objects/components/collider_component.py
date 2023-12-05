

class ColliderComponent:

    def __init__(self):
        self.up = False
        self.right = False
        self.down = False
        self.left = False

        self.left_collision_object = None
        self.right_collision_object = None
        self.up_collision_object = None
        self.down_collision_object = None

        self.all_off = False
        self.pass_through = False
        self.left_off = False
        self.right_off = False
        self.up_off = False
        self.down_off = False

    def reset(self):
        self.up = False
        self.right = False
        self.down = False
        self.left = False

    
