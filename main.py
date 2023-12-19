import pygame
import LevelEditor
from Engine import AnimationEngine, AudioEngine, EnemyEngine, EnvironmentEngine, CollisionEngine, InputEngine, \
    GraphicsEngine, PlayerEngine, PhysicsEngine, ScrollEngine, SpriteEngine, ItemEngine


def main_loop():
    '''Hungarian Notation for type hinting
    e = Engine object
    l = list
    o = object
    d = dictionary
    i = int
    f = float
    '''

    # initialize our engines
    e_inputs = InputEngine.InputsEngine()
    e_graphics = GraphicsEngine.GraphicsEngine()
    e_physics = PhysicsEngine.PhysicsEngine()
    e_player = PlayerEngine.PlayerEngine()
    e_level_editor = LevelEditor.LevelEditor()
    e_sprite = SpriteEngine.SpriteEngine()
    e_collision = CollisionEngine.CollisionEngine()
    e_animation = AnimationEngine.AnimationEngine()
    e_scroll = ScrollEngine.ScrollEngine()
    e_audio = AudioEngine.AudioEngine()
    e_enemy = EnemyEngine.EnemyEngine()
    e_environment = EnvironmentEngine.EnvironmentEngine()
    e_item = ItemEngine.ItemEngine()

    # simulation runtime variables
    l_game_objects = list()
    clock = pygame.time.Clock()
    f_delta_time = 0
    i_fps = 120
    d_events = {'TextInput': None,
                'KeyDown': None,
                'MouseWheel': None}

    # main game loop
    running = True
    while running:

        # capture events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.TEXTINPUT:
                e_level_editor.text_box_ui.event = event
                d_events['TextInput'] = event
            if event.type == pygame.KEYDOWN:
                e_level_editor.text_box_ui.event = event
                d_events['KeyDown'] = event
            if event.type == pygame.MOUSEWHEEL:
                e_level_editor.c_scene.event = event
                e_level_editor.attribute_ui.event = event
                d_events['MouseWheel'] = event

        d_inputs = e_inputs.update()

        e_graphics.update(GameObjectsList=l_game_objects, LevelEditor=e_level_editor, Events=d_events)

        if not e_level_editor.edit:

            for objects in e_graphics.render_buffer:
                e_collision.update(RenderBuffer=e_graphics.render_buffer, CurrentObject=objects)
                e_physics.update(GameObject=objects, DeltaT=f_delta_time)
                e_sprite.update(GameObject=objects, DeltaT=f_delta_time)
                e_player.update(InputDict=d_inputs, PlayerObject=objects, DeltaT=f_delta_time)
                e_enemy.update(GameObject=objects, ScrollEngine=e_scroll)
                e_animation.update(GameObject=objects)
                e_environment.update(GameObject=objects)
                e_item.update(GameObject=objects)
                e_audio.update(GameObject=objects)
                e_scroll.update(GameObject=objects)

        e_scroll.scroll_objects(GameObjects=l_game_objects, LevelEditor=e_level_editor, InputDict=d_inputs)

        e_level_editor.update(InputDict=d_inputs, GameObjects=l_game_objects, GraphicsEngine=e_graphics)

        d_events = {'TextInput': None,
                    'KeyDown': None,
                    'MouseWheel': None}

        f_delta_time = clock.tick(i_fps) / 1000
    pygame.quit()


# entry point
if __name__ == '__main__':
    main_loop()
