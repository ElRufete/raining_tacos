import pygame
from settings import *
from animations import linear_animation


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
        self.index = 0
        self.image = self.image_list[self.index]
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.animation_counter = 0
        self.interval = 4
    
    def update(self):
        self._animate_me()
        self._kill_me()

    def _animate_me(self):
        self.index, self.animation_counter = linear_animation(
            self.image_list, 
            self.interval,
            self.index,
            self.animation_counter
        )
        self.image = self.image_list[self.index]

    def _kill_me(self):
        if self.index >= len(self.image_list) - 1 and self.animation_counter >= self.interval - 1:
            self.kill()

    
class Mist(Smoke):
    def __init__(self, pos):
        super().__init__(pos)
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

        self.image = self.image_list[self.index]
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.midbottom = pos
        self.interval = 5


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


class Fire(pygame.sprite.Sprite):
    def __init__(self, caller):
        super().__init__()
        self.caller = caller
        self.image_list = [
            pygame.image.load('images/effects/fire_1.png').convert_alpha(), 
            pygame.image.load('images/effects/fire_2.png').convert_alpha(), 
            pygame.image.load('images/effects/fire_3.png').convert_alpha(), 
            pygame.image.load('images/effects/fire_4.png').convert_alpha(), 
            pygame.image.load('images/effects/fire_5.png').convert_alpha(), 
            pygame.image.load('images/effects/fire_6.png').convert_alpha(), 
            pygame.image.load('images/effects/fire_7.png').convert_alpha(), 
        ]
        self.index = 0
        self.alpha = 150
        self.image = self.image_list[self.index]
        self.image.set_alpha(self.alpha)
        self.rect = self.image.get_rect()
        self.rect.bottom = self.caller.rect.bottom + 3
        self.rect.centerx = self.caller.rect.centerx
        self.animation_counter = 0
        self.interval = 8

    def update(self):
        self._animate_me()
        self._move()
        self._kill_me()
        
    def _animate_me(self):
        self.index, self.animation_counter = linear_animation(
            self.image_list,
            self.interval,
            self.index,
            self.animation_counter,
        )
        self.image = self.image_list[self.index]
        self.image.set_alpha(self.alpha)

    def _move(self):
        self.rect.bottom = self.caller.rect.bottom + 6
        self.rect.centerx = self.caller.rect.centerx

    def _kill_me(self):
        if not self.caller.alive():
            self.kill()

        
    

