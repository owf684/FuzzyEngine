import pygame


class AudioComponent:

    def __init__(self):
        pygame.mixer.init()
        # this will be used in the audio engine to play queued fx
        self.audio_buffer = list()

        # this will store loaded audio fx
        self.audio_dict = {}

        # this will keep track of audio fx as they triggered
        self.triggered = {}

    def load_audio(self, audio_key, audio_dir_path):
        self.audio_dict[audio_key] = pygame.mixer.Sound(audio_dir_path)
        self.triggered[audio_key] = False
    def queue_audio(self, audio_key):
        self.audio_buffer.append([self.audio_dict[audio_key],audio_key])
        self.triggered[audio_key] = True
 



