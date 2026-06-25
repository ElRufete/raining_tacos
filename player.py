import pygame
from settings import *
from effects import Crumbs
from powerups import Goose, Bunshin

class Player(pygame.sprite.Sprite):
    """Clase que representa al jugador principal"""
    def __init__(self, rt_game):
        # heredar superclase
        super().__init__()
        # rectangulo player
        self.image_list = [
            pygame.image.load('images/personaje/player_0.png'),
            pygame.image.load('images/personaje/player_1.png'),
            pygame.image.load('images/personaje/player_2.png'),
            ]
        self.spice_image_list = [
            pygame.image.load('images/personaje/player_0.png'),
            pygame.image.load('images/personaje/player_1.png'),
            pygame.image.load('images/personaje/player_2.png'),
        ]
        self.animation = 0
        self.image = self.image_list[self.animation]
        self.rect = self.image.get_rect()
        self.rect.center = (window_width // 2, window_heigh - 50)
        self.dash = False
        self.speed = 8
        self.max_spice = 220
        self.spice = 0
        self.animation_counter = 0
        self.speedup_counter = 0
        self.bunshin_active = False
        self.bunshin_counter = 0
        self.status = 'idle'

    def update(self):
        self._move()
        self._dash()
        self._spice_cap()
        

    def _move(self):
        """mueve al jugador de izquierda a derecha"""
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_a] or pressed[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self._animate_me()
            self.image = self.image_list[self.animation]

        elif pressed[pygame.K_d] or pressed[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self._animate_me()
            self.image = self.image_list[self.animation]

        else:
            self.image = self.image_list[1]
            self.animation = 0
            self.animation_counter = 0
        
        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > window_width:
            self.rect.right = window_width

        

    def _dash(self):

        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_SPACE] and self.spice > 0:
            self.speed = 16
            self.spice -= 1
            self.speedup_counter += 1
            

        else:
            self.speed = 8
            self.speedup_counter = 0
            

 
    def _animate_me(self):
        self.animation_counter += 1

        if self.animation_counter == 15:
            self.animation = 1

        if self.animation_counter == 30:
            self.animation = 2

        if self.animation_counter == 45:
            self.animation = 1

        if self.animation_counter == 60:
            self.animation = 0
            self.animation_counter = 0

        if self.bunshin_active == True:
            self.bunshin_counter += 1

        if self.bunshin_counter == 480:
            self.bunshin_counter = 0

    def _spice_cap(self):
        if self.spice >= self.max_spice:
            self.spice = self.max_spice

    def get_goose(self):
        goose = Goose(self.rect.midtop,self)
        geese.add(goose)
        goose_sound.play()

    def get_bunshin(self):
        for offset in (250, -250):
            bunshins.add(Bunshin(self.rect.centerx + offset, self))

    def get_crumbs(self):
        crumbs = Crumbs(self.rect.midtop)
        effects.add(crumbs)

    