import sys
import pygame

sys.path.append('./InputEngine')
sys.path.append("./GraphicsEngine")
sys.path.append('./Objects')
sys.path.append("./PhysicsEngine")
sys.path.append("./PlayerEngine")
sys.path.append('./GameData/GameObjects')
sys.path.append("./LevelEditor")
import input_engine
import graphics_engine
import player_object
import physics_engine
import player_engine
import level_editor


'''Hungarian Notation
e = engine
l = list
o = object
'''
e_inputs = input_engine.InputsEngine()
e_graphics = graphics_engine.GraphicsEngine()
e_physics = physics_engine.PhysicsEngine()
e_player = player_engine.PlayerEngine() 
e_level_editor = level_editor.LevelEditor()
l_editor_ui_elements = list()

l_game_objects = list()
o_player = player_object.PlayerObject()
l_game_objects.append(o_player)





# Start clock
clock = pygame.time.Clock()
# simulation runtime variables
pygame_events = None
delta_t = 0
FPS = 120
		
# main game loop
running = True


while running:

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

  input_dict = e_inputs.main()
  
  e_graphics.main(GameObjectsList=l_game_objects,UIList=l_editor_ui_elements)

  for objects in e_graphics.render_buffer:
    e_physics.main(GameObject=objects,DeltaT=delta_t)
  e_player.main(InputDict=input_dict,PlayerObject=o_player)

  l_editor_ui_elements = e_level_editor.main(InputDict=input_dict,RenderBuffer=e_graphics.render_buffer)
  delta_t = clock.tick(FPS)/1000
 
pygame.quit()




