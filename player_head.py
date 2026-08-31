import pygame
from settings import *

class PlayerHead(pygame.sprite.Sprite):
    def __init__(self, caller):
        super().__init__()

        self.caller = caller
        self.image_list = [
                pygame.image.load('images/personaje/player_head_0.png'),
                pygame.image.load('images/personaje/player_head_1.png'),
                pygame.image.load('images/personaje/player_head_2.png'),
                ]
        self.nom_image = pygame.image.load('images/personaje/player_head_nom.png')
        
        self.image = self.image_list[1]
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.caller.rect.midtop
        heads.add(self)
        
    def update(self):
        self._head_follows_body()
        self._animate_me()
        self._flicker()

    def _head_follows_body(self):
        self.rect.midbottom = self.caller.rect.midtop

        if self.caller.status == 'idle' and self.caller.index == 1:
            self.rect.midbottom = (
                self.caller.rect.left + self.caller.rect.width // 2, self.caller.rect.top + 2
                )

    def _animate_me(self):
        if self.check_close_tacos():
            self.image = self.nom_image

        elif self.caller.status == "moving":
                self.image = self.image_list[self.caller.index]
        
        else:
            self.image = self.image_list[1]

    def check_close_tacos(self):
        self.in_range = False

        range = 90
        x_range = (self.rect.centerx - range, self.rect.centerx + range)

        for taco in tacos:
            if taco.rect.bottom >= window_heigh - 140:
                if x_range[0] <= taco.rect.centerx <= x_range[1]:
                    self.in_range = True
        
        return self.in_range
    
    def _flicker(self):
        if self.caller in bunshins:
            if self.caller.flicker:
                self.image = pygame.Surface((50,30))
                self.image.fill(black)
                self.image.set_colorkey(black)

        

    