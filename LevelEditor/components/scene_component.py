import json
import os
import sys
import glob
import pygame
import shutil
sys.path.append("./Objects/components")
from vector import Vector
import sprite_component
class SceneComponent:

    def __init__(self):
        self.display_info = pygame.display.Info()

        self.b_save_scene = False
        with open("project_file.json",'r') as file:
            self.project_directory = json.load(file)

        self.scene_directory = self.project_directory['current_project']+'/GameData/SceneData/'
        self.working_scene = 0
        self.l_scene_previews = list()
        self.scroll_delta = 0

        # scene preview dimensions, and appearance attributes
        self.scene_bg_color = (70,70,70)
        self.scene_bg_color_selected = (0,100,255)
        self.working_scene_color = (255,255,255)

        scale_factor = 8
        self.x_scale = self.display_info.current_w/scale_factor
        self.y_scale = self.display_info.current_h/scale_factor
        self.x_crop = 400/scale_factor
        self.y_crop = (self.display_info.current_h*.2+15)/scale_factor
        self.y_position = self.display_info.current_h*.8

        self.font = pygame.font.Font(None,36)
        self.font_color = (255,255,255)
        self.d_inputs = None
        self.c_object_creator = None
        self.game_objects = None
        self.e_graphics = None
        self.event = None

    def update(self,**kwargs):
        game_objects = kwargs['GameObjects']
        e_graphics = kwargs['GraphicsEngine']

        self.d_inputs = kwargs['InputDict']
        self.c_object_creator = kwargs['ObjectCreator']
        self.e_graphics = e_graphics
        self.game_objects = game_objects

        if self.b_save_scene:
            self.b_save_scene = False
            self.save_scene(game_objects,e_graphics)

    def save_scene(self,game_objects,e_graphics):
        # get list of scene folders
        l_scenes = glob.glob(self.scene_directory + "*")
        if len(l_scenes) == 0: self.add_scene()

        # clear working scene 
        working_directory=self.scene_directory+"scene_"+str(self.working_scene)
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
        image = pygame.image.load(working_directory+"/preview.png")
        scene_preview_scaled = pygame.transform.scale(image,(self.x_scale,self.y_scale))
        pygame.image.save(scene_preview_scaled,working_directory+"/preview.png")
        self.get_scene_previews()

    def add_scene(self):
        l_scenes = glob.glob(self.scene_directory + "*")
        new_scene = len(l_scenes)
        os.mkdir(self.scene_directory + "scene_" + str(new_scene))
        shutil.copy2("./Assets/UI/Scene/preview.png",self.scene_directory + "scene_" + str(new_scene))
        self.working_scene = len(l_scenes)
        self.get_scene_previews()

    def delete_scene(self):
        try:
            l_scenes = glob.glob(self.scene_directory+"*")
            if len(l_scenes) >=1:
                working_scene_directory = self.scene_directory+"scene_"+str(self.working_scene)
                for files in glob.glob(working_scene_directory+"/*"):
                    os.remove(files)
                os.rmdir(working_scene_directory)

                # rename directories
                l_scenes = glob.glob(self.scene_directory+"*")
                self.sort_scenes(l_scenes)
                i = 0
                for scene in l_scenes:
                    os.rename(scene,self.scene_directory+"scene_"+str(i))
                    i+= 1
                self.get_scene_previews()
                self.working_scene -= 1
                if self.working_scene < 0:
                    self.working_scene = 0
        except Exception as Error: # will error when no scenes left
            print(Error)

    def load_scene(self):
        working_scene_directory = self.scene_directory+"scene_"+str(self.working_scene)
        scene_objects = glob.glob(working_scene_directory+"/*.json")
        self.game_objects.clear()
        self.e_graphics.clear_render_buffer = True

        for object_jsons in scene_objects:
            try:

                with open(object_jsons,'r') as json_file:
                    object_data = json.load(json_file)
                    object_directory = self.project_directory['current_project'] + object_data['object_json_file']
                if object_data is not None:
                    self.game_objects.append(self.c_object_creator.create_new_object(object_directory))
                    self.game_objects[-1].physics.initial_position = Vector(object_data['initial_position.x'],object_data['initial_position.y'])
                    self.game_objects[-1].save_state.initial_position = Vector(object_data['initial_position.x'],object_data['initial_position.y'])
                    self.game_objects[-1].physics.position = self.game_objects[-1].physics.initial_position()
                    self.game_objects[-1].current_sprite.update(self.game_objects[-1].physics.initial_position())
            except Exception as Error:
                print("unable to open file: ", object_jsons)
                print("Error: ", Error)
                print("File: scene_component.py")

    def get_scene_previews(self):
        self.l_scene_previews.clear()
        l_scenes = glob.glob(self.scene_directory+"*")
        self.sort_scenes(l_scenes)
        for scene in l_scenes:
            try:
                preview_sprite = sprite_component.SpriteComponent()
                preview_image_path = scene + "/preview.png"
                preview_sprite.create_sprite(preview_image_path)
                self.l_scene_previews.append(preview_sprite)
            except Exception as Error:
                print(Error)

    def sort_scenes(self,l_scenes):
        i = 0
        j = 0
        while i < len(l_scenes):
            key = int(os.path.basename(l_scenes[i])[6:])
            key_string = l_scenes[i]
            j = i + 1
            while j < len(l_scenes):
                if key > int(os.path.basename(l_scenes[j])[6:]):
                    l_scenes[i] = l_scenes[j]
                    l_scenes[j] = key_string
                    key = int(os.path.basename(l_scenes[i])[6:])
                    key_string = l_scenes[i]
                j += 1
            i += 1

    def draw_scene_previews(self,screen):
        x_position = 128
        mouse_position = pygame.mouse.get_pos()
        for scene_preview in self.l_scene_previews:

            if scene_preview.image is not None:
                scene_name = scene_preview.sprite_path.rstrip("/preview.png")
                scene_name = os.path.basename(scene_name)
                scene_name_image = self.font.render(scene_name, 1, self.font_color)
                scene_preview.update(Vector(x_position+self.scroll_delta,self.y_position+16),\
                                     Vector(self.x_scale-self.x_crop,self.y_scale-self.y_crop))

                # update working scene if new scene selected
                if scene_preview.rect.collidepoint(mouse_position):
                    color = self.scene_bg_color_selected
                    if self.d_inputs['left-click']:
                        self.working_scene = int(scene_name[6:])
                        color = self.working_scene_color
                elif 'scene_' +str(self.working_scene) == scene_name:
                    color = self.working_scene_color
                else:
                    color = self.scene_bg_color


                # update scroll delta
                if mouse_position[0] < self.display_info.current_w*.8 and mouse_position[1] > self.display_info.current_h*.8-15:

                    if self.event is not None:
                        self.scroll_delta += -1*self.event.x*10
                        self.event = None


                crop_rect = pygame.Rect(0, 0, self.x_scale-self.x_crop, self.y_scale-self.y_crop)
                pygame.draw.rect(screen,color, (x_position-8+self.scroll_delta,self.y_position + 8,self.x_scale-self.x_crop+16,self.y_scale-self.y_crop+16))
                pygame.draw.rect(screen,(255,0,0),scene_preview.rect)
                screen.blit(scene_preview.image,(scene_preview.position.x,scene_preview.position.y),crop_rect)
                screen.blit(scene_name_image,(scene_preview.position.x + scene_preview.image_size.x/6 ,scene_preview.position.y+scene_preview.image_size.y))
                x_position += self.x_scale+8