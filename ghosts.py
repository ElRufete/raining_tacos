import pygame


class GhostNTaco(pygame.sprite.Sprite):
    def __init__(self, caller):
        super().__init__()
        self.image = pygame.image.load("images/tacos/ghost/ghost_n_taco.png")
        self.rect = self.image.get_rect()
        self.rect.midbottom = caller.rect.midbottom
        self.speed = 5
        self.alpha = 255
        self.alpha_decrease = 10
        self.image.set_alpha(self.alpha)

    def update(self):
        self._move_up()
        self._vanish()
        self._kill_me()

    def _move_up(self):
        self.rect.y -= self.speed

    def _vanish(self):
        self.alpha -= self.alpha_decrease
        self.image.set_alpha(self.alpha)

    def _kill_me(self):
        if self.alpha <= 0:
            self.kill()
