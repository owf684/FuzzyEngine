import sys
import pygame

sys.path.append('./InputEngine')
sys.path.append("./GraphicsEngine")
sys.path.append('./Objects')
sys.path.append("./PhysicsEngine")
sys.path.append("./PlayerEngine")
sys.path.append('./GameData/GameObjects')
sys.path.append("./LevelEditor")
sys.path.append("./SpriteEngine")
sys.path.append("./CollisionEngine")
sys.path.append("./AnimationEngine")
sys.path.append("./ScrollEngine")

import input_engine
import graphics_engine
import player_object
import physics_engine
import player_engine
import level_editor
import sprite_engine
import collision_engine
import animation_engine
import scroll_engine


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
e_sprite = sprite_engine.SpriteEngine()
e_collision = collision_engine.CollisionEngine()
e_animation = animation_engine.AnimationEngine()
e_scroll  =scroll_engine.ScrollEngine()

l_game_objects = list()


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
    if event.type == pygame.TEXTINPUT:
      e_level_editor.text_box_ui.event = event
    if event.type == pygame.KEYDOWN:
      e_level_editor.text_box_ui.event = event
    if event.type == pygame.MOUSEWHEEL:
      e_level_editor.c_scene.event = event
  input_dict = e_inputs.update()
  
  e_graphics.update(GameObjectsList=l_game_objects, LevelEditor=e_level_editor)

  if not e_level_editor.edit:
    
    for objects in e_graphics.render_buffer:
      e_collision.update(RenderBuffer=e_graphics.render_buffer,CurrentObject=objects)
      e_physics.update(GameObject=objects,DeltaT=delta_t)
      e_sprite.update(GameObject=objects,DeltaT=delta_t)
      e_player.update(InputDict=input_dict,PlayerObject=objects,DeltaT=delta_t)
      e_animation.update(GameObject=objects)
      e_scroll.update(GameObject=objects)

  e_scroll.scroll_objects(GameObjects=l_game_objects,LevelEditor=e_level_editor)

  e_level_editor.update(InputDict=input_dict,GameObjects=l_game_objects,GraphicsEngine=e_graphics)
  delta_t = clock.tick(FPS)/1000
 
pygame.quit()




