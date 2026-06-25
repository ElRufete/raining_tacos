import pygame
from settings import *


class Smoke(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        self.image_list= [
            pygame.image.load("images/smoke/1.png").convert_alpha(),
            pygame.image.load("images/smoke/2.png").convert_alpha(),
            pygame.image.load("images/smoke/3.png").convert_alpha(),
            pygame.image.load("images/smoke/4.png").convert_alpha(),
            pygame.image.load("images/smoke/5.png").convert_alpha(),
            pygame.image.load("images/smoke/6.png").convert_alpha(),
            pygame.image.load("images/smoke/7.png").convert_alpha()
        ]
        self.image = self.image_list[0]
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.counter = 0
        self.animation = 0

    def update(self):
        self._animate_me()

    def _animate_me(self):
        self.counter += 1
        self.image = self.image_list[self.animation]
        self.image.set_colorkey(black)

        if self.counter == 4:
            self.animation += 1
            self.counter = 0

        if self.animation == 6:
            self.animation = 0
            self.kill()

    
class Mist(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        self.image_list = [
            pygame.image.load('images/mist/1.png').convert_alpha(),
            pygame.image.load('images/mist/2.png').convert_alpha(),
            pygame.image.load('images/mist/3.png').convert_alpha(),
            pygame.image.load('images/mist/4.png').convert_alpha(),
            pygame.image.load('images/mist/5.png').convert_alpha(),
            pygame.image.load('images/mist/6.png').convert_alpha(),
            pygame.image.load('images/mist/7.png').convert_alpha(),
            pygame.image.load('images/mist/8.png').convert_alpha(),
            pygame.image.load('images/mist/9.png').convert_alpha(),
        ]

        self.image = self.image_list[0]
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.midbottom = pos
        self.counter = 0
        self.animation = 0

    def update(self):
        self._animate_me()

    def _animate_me(self):

        self.counter += 1
        self.image = self.image_list[self.animation]

        if self.counter == 5:
            self.animation += 1
            self.counter = 0

        if self.animation == 8 and self.counter == 4:
            self.animation = 0
            self.counter = 0
            self.kill()

class Crumbs(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        self.image = pygame.image.load('images/crumbs.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.counter = 0

    def update(self):
        self.counter += 1

        if self.counter == 20:
            self.kill()

        self.rect.y += 2

        if self.rect.bottom == window_heigh:
            self.kill()


class Limon(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load('images/limon.png').convert_alpha()
        self.image.set_colorkey(white)
        pygame.transform.scale(self.image,(45,30))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.counter = 0
        

    def update(self):
        self._die()
        self._flicker()

    def _die(self):

        self.counter += 1
        if self.counter >= fps*2:
            self.kill()

    def _flicker(self):

        if self.counter >= fps:
            if self.counter % 2 == 0:
                self.image = pygame.image.load('images/live_buff.png').convert_alpha()
            else:
                self.image = pygame.image.load('images/limon.png').convert_alpha()
                self.image.set_colorkey(white)
                pygame.transform.scale(self.image,(45,30))
