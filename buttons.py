import pygame

class Button():
    """Clase general para manejar los botones en pantalla"""
    def __init__(self, image,):

        self.image = image
        self.rect = self.image.get_rect()
        self.hovering = False
        self.clicked = False
        self.image_id = 0

    def show(self, surface, x, y,):
        """muestra el botón en la pantalla"""
        self.rect.center = (x, y)
        surface.blit(self.image, (self.rect.x, self.rect.y))
        

    def click(self):
        """comprueba que el botón se ha clicado"""
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

            if pygame.mouse.get_pressed()[0] == 0:

                self.clicked = False

        return action

    def hover(self):
        """comprueba si el puntero está encima del botón"""
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            hovering = True

        else:
            hovering = False

        return hovering
    
    def change_image(self, image):
        """cambia la imagen del botón si el puntero está encima"""
        if self.hover():
            self.image_id = 1
        else:
            self.image_id = 0

        self.image = image[self.image_id]
        

