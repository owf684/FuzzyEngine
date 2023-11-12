import sys
sys.path.append('./Objects')
sys.path.append('./Objects/components')
import game_object
class PlayerObject(game_object.GameObject):

    def __init__(self):
        super().__init__()

        self.current_sprite.create_sprite('./GameData/Assets/PlayerSprites/chris.png')
        self.generic_sprite_1.create_sprite('./GameData/Assets/PlayerSprites/chris.png')

    
        self.save_state.object_json='./GameData/jsons/player_object.json' # needed for creating scenes. 
        #setup some variables
        self.physics.k.x = 100
        self.physics.k.y = 0
    

        #other vairables
        self.player_walking_force = 20000
        self.initial_jump_velocity = -100
        self.jump_velocity_increment = 1000
        self.max_jump_velocity = -240
        self.cap_jump_velocity= False
    def update(self, **kwargs):
        input_dict = kwargs['InputDict']
        delta_t = kwargs['DeltaT']
        self.x_movement(input_dict)
        self.y_movement(input_dict,delta_t)



    def x_movement(self,input_dict):
        self.physics.direction.x = input_dict['horizontal']
        self.physics.force.x = self.player_walking_force*self.physics.direction.x

    def y_movement(self,input_dict,delta_t):
        if input_dict['vertical'] == 1 and not input_dict['vertical_latch'] and self.collider.down:
        
            self.physics.direction.y = input_dict['vertical']
            self.physics.initial_velocity.y = self.initial_jump_velocity
            input_dict['vertical_latch'] = True
        
        elif input_dict['vertical'] == 1 and input_dict['vertical_latch'] and not self.collider.down and not self.cap_jump_velocity:
        
            self.physics.initial_velocity.y -= self.jump_velocity_increment*delta_t
            if (self.physics.initial_velocity.y <= self.max_jump_velocity) or self.collider.up:
                self.cap_jump_velocity = True
        
        elif input_dict['vertical'] == 0 and input_dict['vertical_latch'] :
        
            input_dict['vertical_latch'] = False
            self.physics.direction.y = input_dict['vertical']
            self.cap_jump_velocity = False
    

def create_object():
    return PlayerObject()