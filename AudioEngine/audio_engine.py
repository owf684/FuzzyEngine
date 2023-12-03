import pygame


class AudioEngine:

    def update(self,**kwargs):
        objects = kwargs['GameObject']

        i = 0
        
        for audio in objects.audio.audio_buffer:
            audio[0].play()
            objects.audio.audio_buffer.remove(audio)
