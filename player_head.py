import pygame

class PlayerHead(pygame.sprite.Sprite):
    def __init__(self, caller):
        super().__init__()

        self.caller = caller
        self.image_list = [
                pygame.image.load('images/personaje/player_head_0.png'),
                pygame.image.load('images/personaje/player_head_1.png'),
                pygame.image.load('images/personaje/player_head_2.png'),
                ]
        
        self.image = self.image_list[1]
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.caller.rect.midtop


    def update(self):
        self._head_follows_body()


    def _head_follows_body(self):
        self.rect.midbottom = self.caller.rect.midtop

        if self.caller.status == 'idle' and self.caller.index == 1:
            self.rect.midbottom = (self.caller.rect.left + self.caller.rect.width // 2, self.caller.rect.top + 2)

        

    