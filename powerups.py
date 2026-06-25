import pygame
from settings import *
from effects import Mist, Crumbs
from random import randint
from tacos import NTaco

class Goose(pygame.sprite.Sprite):
    """Un ganso que come tacos a su paso"""
    def __init__(self, pos, player):
        super().__init__()

        self.left_image_list = [
            pygame.image.load('images/goose_left1.png').convert_alpha(),
            pygame.image.load('images/goose_left2.png').convert_alpha(),
        ]
        self.right_image_list = [
             pygame.image.load('images/goose_right1.png').convert_alpha(),
            pygame.image.load('images/goose_right2.png').convert_alpha(),
        ]
        self.animation = 0
        self.image = self.right_image_list[self.animation]
        self.rect = self.image.get_rect()
        self.rect.midbottom = pos
        self.increase_animation = 1

        if player.rect.x <= (window_width // 2):
            self.go_left = True
        if player.rect.x > (window_width // 2):
            self.go_left = False

        self.animation_counter = 0
        

    def update(self):
        self._animate_me()
        self._move_up()
        self._bounce()
        self._kill_me()

    def _animate_me(self):    
        """itera entre los diferentes frames de la animación"""
        self.animation_counter += 1
        if self.animation_counter % 15 == 0:
            self.animation += self.increase_animation
            self.increase_animation *= -1

    def _move_up(self):
        """sube"""
        self.rect.y -= 2.5

    def _bounce(self):
        """rebota al alcancar el borde lateral de la pantalla"""
        if self.rect.left < 0:
            self.go_left = False

        if self.rect.right > window_width:
            self.go_left = True

        if self.go_left == True:
            self.rect.x -= 6
            self.image = self.left_image_list[self.animation]

        if self.go_left == False:
            self.rect.x += 6
            self.image = self.right_image_list[self.animation]

    def get_crumbs(self):
        """deja migas al comerse un taco"""
        if self.go_left:
            self.crumbs = Crumbs(self.rect.midleft)
        else:
            self.crumbs = Crumbs(self.rect.midright)
        effects.add(self.crumbs)
    

           
    def _kill_me(self):
        """elimina el sprite cuando llega a la parte superior"""
        if self.rect.bottom < 0:
            self.kill()

    
class Bunshin(pygame.sprite.Sprite):
    """Clase general para definir una copia del jugador"""
    def __init__(self, x, player):
        super().__init__()

        self.x = x
        self.image = player.image
        self.rect = self.image.get_rect()
        self.rect.bottom = window_heigh
        self.rect.centerx = x
        self.counter = 0
        self.bunshin_counter = 0
        self.bunshin_active = False
        self.flicker = False

    def update(self, player):
        self.image = player.image
        self._call_mist(player)
        self.counter += 1
        self._move(player)
        self._flicker()
        
        
    def _create_mist(self): 
        """crea un efecto de niebla"""   
        mist = Mist(self.rect.midbottom)
        effects.add(mist)

    def _call_mist(self, player):
        """llama al efecto de niebla al aparecer y desaparecer"""
        if self.counter == 0:
            self._create_mist()
            jutsu.play()
            nani.play()
        if self.counter == 480:
            player.bunshin_active = False
            self._create_mist()
            jutsu.play()
            self.kill()
            
            
    def renew(self):
        self.counter = 1
        nani.play()

    def _move(self, player):
        """mueve al bunshin solo si el jugador está en los límites de la pantalla"""
        pressed = pygame.key.get_pressed()

        if player.rect.left > 0 and player.rect.right < window_width:

            if pressed[pygame.K_a] or pressed[pygame.K_LEFT]:
                self.rect.x -= player.speed

            if pressed[pygame.K_d] or pressed[pygame.K_RIGHT]:
                self.rect.x += player.speed

    def _flicker(self):
        """El clon parpadea cuando está a punto de expirar"""

        if (self.counter / 12).is_integer() and self.counter >= 360 and self.counter <= 420:
            self.flicker = True

        elif (self.counter / 4).is_integer() and self.counter > 420:
            self.flicker = True

        else:
            self.flicker = False

        if self.flicker:
            self.image = pygame.Surface((50, 100))
            self.image.fill(black)
            self.image.set_colorkey(black)

    def get_crumbs(self):

            self.crumbs = Crumbs(self.rect.midtop)
            effects.add(self.crumbs)

class Clancy(pygame.sprite.Sprite):
    """Un cangrejo de río que se come los tacos a punto de caer"""
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load('images/clancy.png')
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect()
        self.rect.top = window_heigh
        self.rect.centerx = pos
        self.speed = 6
        self.counter = 0
        self.status = 'go up'

    def update(self):
        self.go_up()
        self.wait()
        self.go_down()

    def go_up(self):
        """sube"""
        if self.status == 'go up':
            self.rect.y -= self.speed

        if self.rect.bottom <= window_heigh:
            self.status = 'idle'

    def wait(self):
        """espera una vez arriba"""
        if self.status == 'idle':
            self.counter += 1

        if self.counter >= 20:
            self.status = 'go down'
            
    def go_down(self):
        """vuelve a bajar si no se ha encontrado ningún taco"""
        if self.status == 'go down':
            self.rect.y += self.speed

        if self.rect.top >= (window_heigh + 5):
            self.kill()

    def get_crumbs(self):
        """deja migas tras comerse un taco"""
        self.crumbs = Crumbs(self.rect.midtop)
        effects.add(self.crumbs)

###ICONS

class GooseIcon(NTaco):
    """icono quer representa el power-up del ganso"""
    def __init__(self, spawner):
        super().__init__(spawner)
        self.image = pygame.image.load("images/eater_buff.png").convert_alpha()
        self.speed = 4
        self.sound = glass
        
    def _crash(self):
        """Si cae al suelo desaparece"""
        if self.rect.bottom > window_heigh:
            self.sound.play()
            self.kill()

class HeartIcon(GooseIcon):
    """Icono que da una vida extra al cogerlo"""
    def __init__(self,spawner):
        super().__init__(spawner)
        self.image = pygame.image.load("images/live_buff.png").convert_alpha()

class BunshinIcon(GooseIcon):
    """icono que genera clones del jugador durante un timepo al cogerlo"""
    def __init__(self, spawner):
        super().__init__(spawner)
        self.image = pygame.image.load("images/bunshin_buff.png").convert_alpha()

class LimonIcon(GooseIcon):
    """Icono que al cogerlo, convierte los tacos en limones"""
    def __init__(self,spawner):
        super().__init__(spawner)
        self.image = pygame.image.load("images/limon_icon.png").convert_alpha()
        self.image.set_colorkey(white)

class ClancyIcon(GooseIcon):
    """Icono que al cogerlo invoca a Clancy durante un tiempo"""
    def __init__(self,spawner):
        super().__init__(spawner)
        self.image = pygame.image.load("images/clancy_icon.png").convert_alpha()
        self.image.set_colorkey(white)

class PepperIcon(GooseIcon):
     """icono que otorga spice al cogerlo"""
     def __init__(self,spawner):
        super().__init__(spawner)
        self.image = pygame.image.load("images/pepper_icon.png").convert_alpha()
        self.image.set_colorkey(white)

class DoubleIcon(GooseIcon):
    """icono que duplica la puntuación de los tacos durante un tiempo"""
    def __init__(self,spawner):
        super().__init__(spawner)
        self.image = pygame.image.load("images/2x1.png").convert_alpha()
        self.image.set_colorkey(white)




