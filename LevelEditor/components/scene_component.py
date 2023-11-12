import json
import os
import glob
import pygame

class SceneComponent:

    def __init__(self):
        self.b_save_scene = False
        self.scene_direcotry = './GameData/SceneData/'
        self.working_scene = 0

    def update(self,**kwargs):
        game_objects = kwargs['GameObjects']
        e_graphics = kwargs['GraphicsEngine']

        if self.b_save_scene:
            self.b_save_scene = False
            self.save_scene(game_objects,e_graphics)

    def save_scene(self,game_objects,e_graphics):
        # get list of scene folders
        l_scenes = glob.glob(self.scene_direcotry + "*")
        if len(l_scenes) == 0: self.add_scene()

        # clear working scene 
        working_directory=self.scene_direcotry+"scene_"+str(self.working_scene)
        l_json_objs = glob.glob(working_directory+"/*")
        try:
            for objs in l_json_objs:
                os.remove(objs)
        except Exception as Error:
            print(Error)
        
        # save object data into dict and dump dict into jsons inside working direcotry
        i = 0
        for objects in game_objects:
            save_data = {
                'initial_position.x' : objects.save_state.initial_position.x,
                'initial_position.y': objects.save_state.initial_position.y,
                'object_json_file': objects.save_state.object_json_file
            }
            with open(working_directory+"/object_"+ str(i)+".json", "w") as json_file:
                json.dump(save_data,json_file)
                i += 1
        pygame.image.save(e_graphics.screen,working_directory+"/preview.png")
    def add_scene(self):
        l_scenes = glob.glob(self.scene_direcotry + "*")
        new_scene = len(l_scenes)
        os.mkdir(self.scene_direcotry + "scene_" + str(new_scene))
        self.working_scene = 0