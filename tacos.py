import pygame
from random import randint
from settings import *
from effects import *
from status import Game_Status
from animations import linear_animation, spring_animation


# TACO NORMAL
class NTaco(pygame.sprite.Sprite,):
    """Un taco normal que simplemente cae"""
    # sprite del jugador
    def __init__(self, spawner):
        # heredar superclase
        super().__init__()
        # rectangulo player
        self.gs = spawner.gs
        self.image_list = [
            pygame.image.load('images/tacos/n_taco/n_taco_0.png').convert_alpha(),
            pygame.image.load('images/tacos/n_taco/n_taco_1.png').convert_alpha(),
            pygame.image.load('images/tacos/n_taco/n_taco_2.png').convert_alpha(),
            pygame.image.load('images/tacos/n_taco/n_taco_3.png').convert_alpha(),
        ]
        self.index = 0
        self.image = self.image_list[self.index]
        self.animation_counter = 0
        self.animation_interval = 10
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
        self._animate_me()
        self._fall()
        self._crash()
        self._limon_event()
        
    def _animate_me(self):   
        self.index, self.animation_counter = linear_animation(
            self.image_list, 
            self.animation_interval, 
            self.index, 
            self.animation_counter, 
            )
        self.image = self.image_list[self.index]

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
        
        self.speed = 4
        self.x_speed = 5
        
        self.bounce_counter = 0
        self.bounce_cycle = 80
        self.go_left = False

        self.increase = 1
        self.interval = 10

        self.right_image_list = [
            pygame.image.load(
                "images/tacos/b_taco/b_taco_right/b_taco_right_1.png").convert_alpha(),
            pygame.image.load(
                "images/tacos/b_taco/b_taco_right/b_taco_right_2.png").convert_alpha(),
            pygame.image.load(
                "images/tacos/b_taco/b_taco_right/b_taco_right_3.png").convert_alpha(),
            pygame.image.load(
                "images/tacos/b_taco/b_taco_right/b_taco_right_4.png").convert_alpha(),
        ]
        self.left_image_list = [
            pygame.image.load(
                "images/tacos/b_taco/b_taco_left/b_taco_left_1.png").convert_alpha(),
            pygame.image.load(
                "images/tacos/b_taco/b_taco_left/b_taco_left_2.png").convert_alpha(),
            pygame.image.load(
                "images/tacos/b_taco/b_taco_left/b_taco_left_3.png").convert_alpha(),
            pygame.image.load(
                "images/tacos/b_taco/b_taco_left/b_taco_left_4.png").convert_alpha(),
        ]
        self.right_image = self.right_image_list[0]
        self.left_image = self.left_image_list[0]

        self.rect.x = randint(
            0, window_width - self.rect.width - (self.x_speed * (self.bounce_cycle // 2)))

    def update(self):
        self._fall()
        self._bounce()
        self._animate_me()
        self._crash()
        self._limon_event()

    def _bounce(self):
        '''El taco se mueve de izquierda a derecha'''
        self.bounce_counter += 1
        if not self.go_left:
            self.rect.x += self.x_speed
            
        if self.bounce_counter >= self.bounce_cycle // 2:
            self.go_left = True

        if self.go_left:
            self.rect.x -= self.x_speed

        if self.bounce_counter >= self.bounce_cycle:
            self.go_left = False
            self.bounce_counter = 0

    def _check_direction(self):
        direction = "left" if self.go_left else "right"
        return direction
    
    def _animate_me(self):
        direction = self._check_direction()

        self.index, self.animation_counter, self.increase = spring_animation(
                        self.left_image_list,
                        self.interval,
                        self.index,
                        self.animation_counter,
                        self.increase
                    )
        
        if direction == "left":
            self.image = self.left_image_list[self.index]

        if direction == "right":
            self.image = self.right_image_list[self.index]


class STaco(NTaco):
    """Speedy taco, un taco que cae a toda velocidad"""
    def __init__(self,spawner):
        super().__init__(spawner)

        self.image_list = [
            pygame.image.load("images/tacos/s_taco/s_taco_0001.png").convert_alpha(),
            pygame.image.load("images/tacos/s_taco/s_taco_0002.png").convert_alpha(),
            pygame.image.load("images/tacos/s_taco/s_taco_0003.png").convert_alpha(),
            pygame.image.load("images/tacos/s_taco/s_taco_0004.png").convert_alpha(),
        ]
        self.image = self.image_list[0]
        self.speed = 7
        self._call_fire()

    def update(self):
        self._animate_me()
        self._fall()
        self._crash()
        self._limon_event()

    def _call_fire(self):
        self.fire = Fire(self)
        effects.add(self.fire)


class MTaco(NTaco):
    """Meditaco, un taco que se teletransporta durante la caida"""
    def __init__(self,spawner):
        super().__init__(spawner)
        self.image_list = [
            pygame.image.load("images/tacos/m_taco/m_taco_1.png").convert_alpha(),
            pygame.image.load("images/tacos/m_taco/m_taco_2.png").convert_alpha(),
            pygame.image.load("images/tacos/m_taco/m_taco_3.png").convert_alpha(),
            pygame.image.load("images/tacos/m_taco/m_taco_4.png").convert_alpha(),
        ]
        self.image = self.image_list[0]
        self.rect.x = randint(100, window_width - 100)
        self.counter = 0
        self.sprite_counter = 0
        self.teleport = False

    def update(self):
        self._fall()
        self._set_bounds()
        self._animate_me()
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

        



