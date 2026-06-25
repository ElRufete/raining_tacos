import pygame
from settings import *
from random import randint

class Cloud(pygame.sprite.Sprite):
    """Clase para manejar las nubes delanteras
      del menú principal"""
    def __init__(self,pos):
        super().__init__()
        self.image = pygame.image.load(
            f"images/clouds/cloud_{randint(1,5)}.png").convert_alpha()
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect()
        self.rect.x = randint(-50, window_width - 100 )
        self.rect.top = pos
        self.speed = 2
        
    def update(self):
        self._go_up()
        self._kill_me()

    def _go_up(self):
        self.rect.y -= self.speed

    def _kill_me(self):
        if self.rect.bottom < 0:
            self.kill()

class BackCloud(Cloud):
    """Clase para manejar las nubes traseras
      del menú principal"""
    def __init__(self, pos):
        super().__init__(pos)

        self.image = pygame.image.load(
            f"images/clouds/bg_cloud_{randint(1,5)}.png").convert_alpha()
        self.image.set_colorkey(white)
        self.speed = 1

        
