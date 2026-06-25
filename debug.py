import pygame
from settings import *

class Debug():
    
    def __init__(self,caller):
        self.screen = caller.screen
        self.screen_rect = self.screen.get_rect()

   
    def show(self, var, font = comic, color = white, size = 30,):
        style = pygame.font.Font(font, size)
        surface = style.render(str(var), True, color)
        rectangle = surface.get_rect()
        rectangle.topright = self.screen_rect.topright
        self.screen.blit(surface, rectangle)