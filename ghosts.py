import pygame


class GhostNTaco(pygame.sprite.Sprite):
    def __init__(self, caller):
        super().__init__()
        self.image = pygame.image.load(
            "images/tacos/ghost/ghost_n_taco.png"
        ).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.midbottom = caller.rect.midbottom
        self.speed = 3
        self.alpha = 255
        self.alpha_decrease = 6
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


class GhostBTaco(GhostNTaco):
    def __init__(self, caller):
        super().__init__(caller)
        self.l_image = pygame.image.load(
            "images/tacos/ghost/ghost_b_taco_l.png"
        ).convert_alpha()
        self.r_image = pygame.image.load(
            "images/tacos/ghost/ghost_b_taco_r.png"
        ).convert_alpha()
        self.image = self.l_image
        self.rect = self.image.get_rect()
        self.rect.midbottom = caller.rect.midbottom
        self.caller = caller

    def update(self):
        self._move_up()
        self._vanish()
        self._check_direction()
        self._kill_me()

    def _check_direction(self):
        if not self.caller.go_left:
            self.image = self.r_image


class GhostSTaco(GhostNTaco):
    def __init__(self, caller):
        super().__init__(caller)
        self.image = pygame.image.load(
            "images/tacos/ghost/ghost_s_taco.png"
        ).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.midbottom = caller.rect.midbottom


class GhostMTaco(GhostNTaco):
    def __init__(self, caller):
        super().__init__(caller)
        self.image = (
            pygame.image.load("images/tacos/ghost/ghost_m_taco.png")
            .convert_alpha()
            .convert_alpha()
        )
        self.rect = self.image.get_rect()
        self.rect.midbottom = caller.rect.midbottom
