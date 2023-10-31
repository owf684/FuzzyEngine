import pygame    
class ObjectPlacerComponent:

    def update(self,**kwargs):
        d_inputs = kwargs['InputDict']
        game_objects = kwargs['GameObjects']
        level_editor = kwargs['ALevelEditor']

        self.place_object( d_inputs, game_objects ,level_editor )

    def place_object(self,d_inputs,game_objects,level_editor):
        mouse_position = pygame.mouse.get_pos()

        if level_editor.edit and d_inputs['left-click'] and not d_inputs['left_click_latch']:
            d_inputs['left_click_latch'] = True

            obj = level_editor.c_object_creator.create_selected_object()

            if 0 < mouse_position[0] < level_editor.grid.screen_width and \
                0 < mouse_position[1] < level_editor.grid.screen_height:

                # check if object is already there is there?
                if not self.object_exists(mouse_position,game_objects):
                    self.update_position(mouse_position,obj,game_objects,level_editor)


        elif not d_inputs['left-click'] and d_inputs["left_click_latch"]:
            d_inputs["left_click_latch"] = True

    def object_exists(self,mouse_position,game_objects):
        for objects in game_objects:
            if objects.current_sprite.rect.collidepoint(mouse_position):
                return True
        return False
    def update_position(self,mouse_position,obj,game_objects,level_editor):
        snap_position = [0,0]
       
        if mouse_position[0] < level_editor.grid.grid_size:
            snap_position[0] = 0
        else:
            snap_position[0] = int((mouse_position[0] - abs(level_editor.grid.scroll_delta))/level_editor.grid.grid_size)*level_editor.grid.grid_size + abs(level_editor.grid.scroll_delta)                
            snap_position[1] = int(mouse_position[1]/level_editor.grid.grid_size)*level_editor.grid.grid_size
            game_objects.append(obj)
            game_objects[-1].physics.initial_position.x = snap_position[0]
            game_objects[-1].physics.initial_position.y = snap_position[1]
            game_objects[-1].physics.position = game_objects[-1].physics.initial_position()
            game_objects[-1].current_sprite.position.x = snap_position[0]
            game_objects[-1].current_sprite.position.y = snap_position[1]