import sys
sys.path.append('./Objects')
sys.path.append('./Objects/components')
import game_object
from vector import Vector
class PlayerObject(game_object.GameObject):

    def __init__(self):
        super().__init__()

        self.current_sprite.create_sprite('./GameData/Assets/PlayerSprites/mario/mario_idle_right.png')
        self.generic_sprite_1.create_sprite_sheet('./GameData/Assets/PlayerSprites/mario/mario_run_right.png',3,Vector(32,32))
        self.generic_sprite_1.position = Vector(0,0)
        self.generic_sprite_1.create_sprite_sheet_rect()
        self.generic_sprite_2.create_sprite('./GameData/Assets/PlayerSprites/mario/mario_idle_right.png')
        self.generic_sprite_3.create_sprite('./GameData/Assets/PlayerSprites/mario/mario_jump_right.png')
        self.animator.frame_count = 3
        self.animator.frame_duration = 90
    
        self.save_state.object_json_file='./GameData/jsons/player_object.json' # needed for creating scenes. 
        #setup some variables
        self.physics.k.x = 100
        self.physics.k.y = 0
    

        #other vairables
        self.player_walking_force = 20000
        self.initial_jump_velocity = -100
        self.jump_velocity_increment = 1000
        self.max_jump_velocity = -240
        self.cap_jump_velocity= False
        self.jumping = False

        self.audio_dir ="./GameData/Assets/Audio"

        self.audio.load_audio('small-jump', self.audio_dir+"/MarioFX/smb_jump-small.wav")

    def update(self, **kwargs):
        # get relevant variables
        input_dict = kwargs['InputDict']
        delta_t = kwargs['DeltaT']

        # update object
        self.x_movement(input_dict)
        self.y_movement(input_dict, delta_t)
        self.animation_handler(input_dict)
        self.audio_handler()


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
    
    def animation_handler(self,input_dict):
        # update direction
        self.animator.set_direction(self.physics)

        # reset jump animation
        if self.jumping and self.collider.down:
            self.jumping = False

        if not self.jumping:

            # walk animation
            if abs(input_dict['horizontal']) > 0:
                self.animator.trigger_generic_animation(1)

            # idle animation
            elif input_dict['horizontal'] == 0:
                self.animator.trigger_generic_animation(2)

            # set jump flag
            if input_dict['vertical'] == 1 and self.collider.down:
                self.jumping = True

        # jump animation
        if self.jumping and not self.collider.down:
            self.animator.trigger_generic_animation(3)

    def audio_handler(self):

        # jump audio
        if self.jumping and self.collider.down and not self.audio.triggered['small-jump']:
            self.audio.queue_audio('small-jump')

        if not self.jumping and self.collider.down:
            self.audio.triggered['small-jump'] = False



def create_object():
    return PlayerObject()