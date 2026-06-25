import pygame
from random import randint
from settings import *
from effects import *
from status import Game_Status


# TACO NORMAL
class NTaco(pygame.sprite.Sprite,):
    """Un taco normal que simplemente cae"""
    # sprite del jugador
    def __init__(self, spawner):
        # heredar superclase
        super().__init__()
        # rectangulo player
        self.gs = spawner.gs
        self.image = pygame.image.load(
            'images/n_taco.png').convert_alpha()
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.speed = 5 
        self.rect.bottom = 0
        self.rect.x = randint(1, window_width - 150)
        self.sound = taco_fall
        self.islimon = False
        self.limon_counter = 0
        self.limon_thresshold = randint(10, 35)
        self.limon_sound = limon_sounds[randint(0,1)]

        


    def update(self):
        self._fall()
        self._crash()
        self._limon_event()

    def _fall(self):
        """caída"""
        self.rect.y += self.speed
    def _crash(self):
        """si cae al suelo, desaparece, resta una vida y deja un splat"""
        if self.rect.bottom > window_heigh:
            self.kill()
            self.gs.lives -= 1
            taco_fall.play()
            splat = Splat(self.rect.center)
            effects.add(splat)

    def _limon_event(self):
        """Evento que ocurre al adquirir el power-up limón,los tacos 
        en pantalla se convierten en un limón y dan una vida al jugador"""

        if self.islimon:
            self.limon_counter +=1
            if self.limon_counter == self.limon_thresshold:
                self.gs.score += 1
                self.gs.lives += 1
                self.smoke = Smoke(self.rect.center)
                self.limon = Limon(self.rect.center)
                effects.add(self.smoke)
                limons.add(self.limon)
                self.limon_sound.play()
                self.kill()


class BTaco(NTaco):
    """Balloon taco: Un taco que se balancea por la pantalla"""
    def __init__(self,spawner):
        super().__init__(spawner) 
        self.rect.x = randint(0, window_width - 270)
        self.speed = 4
        self.bounce_counter = 0
        self.go_left = False
        self.right_image = pygame.image.load(
                "images/b_taco_right.png").convert_alpha()
        self.left_image = pygame.image.load(
                "images/b_taco_left.png").convert_alpha()

    def update(self):
        self._fall()
        self._bounce()
        self._crash()
        self._limon_event()

    def _bounce(self):
        '''El taco se mueve de izquierda a derecha'''
        self.bounce_counter += 1
        if self.go_left == False:
            self.rect.x += 8
            self.image = self.right_image

        if self.bounce_counter >= 30:
            self.go_left = True

        if self.go_left:
            self.rect.x -= 8
            self.image = self.left_image

        if self.bounce_counter >= 60:
            self.go_left = False
            self.bounce_counter = 0

class STaco(NTaco):
    """Speedy taco, un taco que cae a toda velocidad"""
    def __init__(self,spawner):
        super().__init__(spawner)
        
        self.image = pygame.image.load(
            "images/s_taco.png").convert_alpha()
        self.speed = 7

    def update(self):
        self._fall()
        self._crash()
        self._limon_event()

class MTaco(NTaco):
    """Meditaco, un taco que se teletransporta durante la caida"""
    def __init__(self,spawner):
        super().__init__(spawner)
        self.image = pygame.image.load(
            "images/m_taco.png").convert_alpha()
        self.rect.x = randint(100, window_width - 100)
        self.counter = 0
        self.sprite_counter = 0
        self.teleport = False

    def update(self):
        self._fall()
        self._set_bounds()
        self._teleport()
        self._create_smoke()
        self._crash()
        self._limon_event()

    def _set_bounds(self):
            """impide que se salga de la pantalla"""
            if self.rect.right > window_width:
                self.rect.right = window_width
            if self.rect.left < 0:
                self.rect.left = 0


    def _teleport(self):
        """Se teletransporta aleatoriamente a izquierda o derecha"""
        self.counter += 1
        if self.counter == 90:
            self.rect.x += randint(-350, 350)
            

    def _create_smoke(self):
        """Crea una nube de humo al teletransportarse"""
        if self.counter == 89:
            smoke = Smoke(self.rect.center)
            effects.add(smoke)
        if self.counter == 91:
            smoke = Smoke(self.rect.center)
            effects.add(smoke)
            


class Splat(pygame.sprite.Sprite):
    """una mancha de barro que aparece si un taco cae al suelo"""
    def __init__(self, pos):
        super().__init__()

        self.image = pygame.image.load(
            "images/splat.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.counter = 0

    def update(self):
        self.counter += 1
        if self.counter == 25:
            self.kill()

class IntroTaco(pygame.sprite.Sprite):
    """un taco que cae como transición al menú principal"""
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(
            'images/taco_intro.png').convert_alpha()
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect()
        self.rect.centerx = window_width // 2
        self.rect.bottom = 0
        self.speed = 14

    def update(self):
        self.rect.y += self.speed

class BalloonBoy(pygame.sprite.Sprite):
    """jumpscare de Balloon Boy que aparece si se pulsa 10 veces
    el botón oculto en las instrucciones"""
    def __init__(self, caller):
        super().__init__()
        self.image = pygame.image.load(
            'images/_balloon_boy.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.midtop = caller.screen_rect.midbottom
        self.animation_counter = 0
        self.rumble = False
        self.rumble_range = 8
        self.speed = 95

    def update(self):
        if not self.rumble:
            self._go_up()
            if self.rect.bottom <= window_heigh + 20:
                self.rumble = True
        self._rumble()
        if self.rumble:
            self._limit_rumble()
        self._kill_me()

    def _go_up(self):
        """sube"""
        self.rect.y -= self.speed

    def _rumble(self):
        """Al terminar de subir, Balloon boy tiembla y suena un grito"""
        if self.rumble:
            self.animation_counter += 1
            if self.animation_counter % 2 == 0:
                    self.rect.x += randint(
                        -self.rumble_range, self.rumble_range)
                    self.rect.y += randint(
                        -self.rumble_range, self.rumble_range)

    def _limit_rumble(self):
        """impide que el sprite se vaya demasiado lejos debido al rumble"""
        if self.rect.bottom < window_heigh:
            self.rect.bottom = window_heigh
        if self.rect.bottom > window_heigh + 10:
            self.rect.bottom = window_heigh + 10
        if self.rect.centerx < (window_width // 2) - 5:
            self.rect.centerx = (window_width // 2) - 5
        if self.rect.centerx > (window_width // 2) + 5:
            self.rect.centerx = (window_width // 2) + 5


    def _kill_me(self):
        """Baloon Boy desaparece al final del jumpscare"""
        if self.animation_counter >= 120:
            self.kill()

        



