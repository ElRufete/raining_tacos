import pygame

class Music():
    def __init__(self, music_file):
        pygame.mixer.init()
        self.music_file = music_file

    def play_music(self,volume = 0.4, loops = -1):
        pygame.mixer.music.load(self.music_file)
        pygame.mixer.music.play(loops)
        pygame.mixer.music.set_volume(volume)
        
    def pause_music(self):
        pygame.mixer.music.pause()

    def resume_music(self):
        pygame.mixer.music.unpause()

    def stop_music(self):
        pygame.mixer.music.stop()