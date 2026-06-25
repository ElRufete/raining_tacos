import pygame
from settings import *
from player import Player
from status import Game_Status
from buttons import Button
from powerups import Bunshin

class UI():
    """Clase para manejar los elementos de interfaz"""
    def __init__(self,rt_game):

        self.player = rt_game.player
        self.gs = rt_game.gs
        self.spawner = rt_game.spawner
        self.screen = rt_game.screen
        self.screen_rect = rt_game.screen_rect
        self.inst = rt_game.inst
        self.logo_alpha = 0

        self.background = pygame.Surface(
            (window_width, 50)).convert_alpha()
        self.background_rect = self.background.get_rect()
        self.background.fill(black)
        self.background.set_alpha(50)
        self.pause_blackout = pygame.Surface(
            (window_width, window_heigh)).convert_alpha()
        self.pause_blackout_rect = self.pause_blackout.get_rect()
        self.pepper_icon = pygame.image.load(
            'images/pepper_icon.png').convert_alpha()
        self.heart_icon = pygame.image.load(
            'images/live_buff.png').convert_alpha()
        self.taco_icon = pygame.image.load(
            'images/n_taco.png').convert_alpha()
        self.clancy_icon = pygame.image.load(
            'images/clancy_icon.png').convert_alpha()
        self.clancy_icon.set_colorkey(white)
        self.double_icon = pygame.image.load(
            'images/2x1.png').convert_alpha()
        self.double_icon.set_colorkey(white)
        self.pepper_rect = self.pepper_icon.get_rect()

        self.go_image = pygame.image.load(
                "images/taco_game_over.png"
                ).convert_alpha()
        self.go_image.set_colorkey(white)
        self.go_image_rect = self.go_image.get_rect()
        self.go_image_rect.midbottom = self.screen_rect.midbottom

        self.menu_image = pygame.image.load(
            'images/taco_intro.png').convert_alpha()
        self.menu_image.set_colorkey(white)
        self.menu_image_rect = self.menu_image.get_rect()
        self.menu_image_rect.centerx = self.screen_rect.centerx
        self.menu_image_rect.bottom = self.screen_rect.bottom - 30

        self.title = pygame.image.load(
            'images/title_image.png').convert_alpha()
        self.title_rect = self.title.get_rect()
        self.title_rect.centerx = self.screen_rect.centerx
        self.title_rect.y = 50

        self.logo = pygame.image.load(
            'images/Fondos/nevermore_logo.png').convert_alpha()
        self.logo_rect = self.logo.get_rect()
        self.logo_rect.center = self. screen_rect.center
        self.logo.set_alpha(self.logo_alpha)
        

        #BUTTON IMAGES
        
        self.play_img = [
            pygame.image.load(
                "images/_buttons/_play_0.png"
                ).convert_alpha(), 
            pygame.image.load(
                "images/_buttons/_play_1.png"
                ).convert_alpha()]
        self.play_again_img = [
            pygame.image.load(
                "images/_buttons/_play_again_0.png"
                ).convert_alpha(), 
            pygame.image.load(
                "images/_buttons/_play_again_1.png"
                ).convert_alpha()]
        self.quit_img = [
            pygame.image.load(
                "images/_buttons/_quit_0.png"
                ).convert_alpha(), 
            pygame.image.load(
                "images/_buttons/_quit_1.png"
                ).convert_alpha()]
        self.resume_img = [
            pygame.image.load(
                "images/_buttons/_resume_0.png"
                ).convert_alpha(), 
            pygame.image.load(
                "images/_buttons/_resume _1.png"
                ).convert_alpha()]
        self.restart_img = [
            pygame.image.load(
                "images/_buttons/_restart_0.png"
                ).convert_alpha(), 
            pygame.image.load(
                "images/_buttons/_restart_1.png"
                ).convert_alpha()]
        self.menu_img = [
            pygame.image.load(
                "images/_buttons/_back_to_menu_0.png"
                ).convert_alpha(), 
            pygame.image.load(
                "images/_buttons/_back_to_menu_1.png"
                ).convert_alpha()]
        self.htp_img = [
            pygame.image.load(
                'images/_buttons/_how_to_play_0.png'
                ).convert_alpha(),
            pygame.image.load(
                'images/_buttons/_how_to_play_1.png'
                ).convert_alpha()]
        self.l_arrow_img = pygame.image.load(
                'images/_buttons/_arrow.png').convert_alpha()
        self.r_arrow_img = pygame.transform.flip(
            self.l_arrow_img,True, False)
        self.hidden_img = pygame.Surface((60, 42)).convert_alpha()
        self.hidden_img.set_colorkey(black)
        
        
        ##BUTTONS##

        self.resume_bt = Button(self.resume_img[0])
        self.quit_bt = Button(self.quit_img[0])
        self.play_again_bt = Button(self.play_again_img[0])
        self.play_bt = Button(self.play_img[0],)
        self.restart_bt = Button( self.restart_img[0])
        self.menu_bt = Button(self.menu_img[0])
        self.htp_bt = Button(self.htp_img[0])
        self.l_arrow_bt = Button(self.l_arrow_img)
        self.r_arrow_bt = Button(self.r_arrow_img)
        self.hidden_bt = Button(self.hidden_img)
        
       
    def blit_me(self):
        """muestra los elementos en pantalla"""
        if self.gs.status == "gameplay":
            self.screen.blit(self.background, self.screen_rect.topleft)
            self.show_spice_bar()
            self.show_lives()
            self.show_score()
            if self.spawner.clancy_active:
                self.show_clancy_bar()
            if self.gs.double:
                self.show_double_bar()

        if self.gs.status == "intro":
            self._show_logo()
            self._limit_alpha()
            self._intro_text()

        if self.gs.status == "menu":
            self.screen.blit(self.menu_image,self.menu_image_rect)
            self.screen.blit(self.title, self.title_rect)
            self.play_bt.show(self.screen,
                self.screen_rect.centerx,self.screen_rect.centery - 120)
            self.play_bt.change_image(self.play_img)
            self.quit_bt.show(self.screen,
                self.screen_rect.centerx,self.screen_rect.centery - 60)
            self.quit_bt.change_image(self.quit_img)
            self.htp_bt.show(self.screen,
                self.screen_rect.centerx,self.screen_rect.centery)
            self.htp_bt.change_image(self.htp_img)
                             
        if self.gs.status == "instructions":
            self.menu_bt.show(self.screen,
                self.screen_rect.centerx,self.screen_rect.bottom - 40)
            self.menu_bt.change_image(self.menu_img)
            if self.inst.index != 0:
                self.l_arrow_bt.show(self.screen,
                    self.screen_rect.left + 75, window_heigh - 40)
            if self.inst.index != 2:
                self.r_arrow_bt.show(self.screen,
                    self.screen_rect.right - 75, window_heigh - 40)
            if self.inst.index == 1:
                self.hidden_bt.show(self.screen, 75, 305)

        if self.gs.status == "pause":
             self.pause_blackout.set_alpha(120)
             self.screen.blit(self.pause_blackout, 
                              self.screen_rect.topleft)
             self.show_text(
                self.screen, comic, "PAUSE", white,
                70, self.screen_rect.centerx, self.screen_rect.top + 200)
             
             self.resume_bt.show(self.screen,
                self.screen_rect.centerx,self.screen_rect.centery,)
             self.resume_bt.change_image(self.resume_img)
             self.restart_bt.show(self.screen,
                self.screen_rect.centerx,(self.screen_rect.centery + 75))
             self.restart_bt.change_image(self.restart_img)
             self.quit_bt.show(self.screen,
                self.screen_rect.centerx,(self.screen_rect.centery + 225))
             self.quit_bt.change_image(self.quit_img)
             self.menu_bt.show(self.screen,
                self.screen_rect.centerx,(self.screen_rect.centery + 150))
             self.menu_bt.change_image(self.menu_img)
             

        if self.gs.status == "game over":
            self.pause_blackout.set_alpha(255)
            self.screen.blit(self.pause_blackout, self.screen_rect.topleft)
            self.screen.blit(self.go_image, self.go_image_rect)
                    
            self.show_text(
            self.screen, comic, "GAME OVER", white,
              70, self.screen_rect.centerx, self.screen_rect.top + 50)
            
            self.show_text(
            self.screen, comic, f'YOUR SCORE: {str(self.gs.score)}', white,
              40, self.screen_rect.centerx, self.screen_rect.top + 150)
            
            self.show_text(
            self.screen, comic, f'TOP SCORE: {str(self.gs.high_score)}', white,
              40, self.screen_rect.centerx, self.screen_rect.top + 225)
            self.quit_bt.show(self.screen,
                self.screen_rect.centerx,self.screen_rect.centery)
            self.quit_bt.change_image(self.quit_img)
            self.play_again_bt.show(self.screen,
                self.screen_rect.centerx,(self.screen_rect.centery - 60))
            self.play_again_bt.change_image(self.play_again_img)
            self.menu_bt.show(self.screen,
            self.screen_rect.centerx,(self.screen_rect.centery + 60))
            self.menu_bt.change_image(self.menu_img)
        

            ##### GAMEPLAY BAR METHODS #######

    def show_spice_bar(self):
        self.screen.blit(
            self.pepper_icon, (25, (self.background_rect.top + 10)))
        self.create_bar(
            self.screen,self.player.spice,
            self.player.max_spice, 65, self.background_rect.top + 15,
                200, 19 )
        
    def show_lives(self):
        self.screen.blit(
            pygame.transform.scale(self.heart_icon, (35, 35)),
              (300, self.background_rect.top + 10))
        self.show_text(
            self.screen, comic, str(self.gs.lives), white,
              30, 355, self.background_rect.top + 25)
        
    def show_score(self):
        self.screen.blit(
            pygame.transform.scale(self.taco_icon, (40, 30)),
              (400, self.background_rect.top + 10))
        self.show_text(
            self.screen, comic, str(self.gs.score), white,
              30, 460, self.background_rect.top + 25)
        
    def show_clancy_bar(self):
        self.screen.blit(
            pygame.transform.scale(self.clancy_icon, (25, 35)),
              (510, self.background_rect.top + 7))
        self.create_bar(
            self.screen,self.spawner.clancy_counter,
            self.spawner.max_clancy_counter, 
            550, self.background_rect.top + 15,
                150, 19 )
        
    def show_double_bar(self):
        self.screen.blit(
            pygame.transform.scale(self.double_icon, (35, 25)),
              (710, self.background_rect.top + 12))
        self.create_bar(
            self.screen,self.gs.double_counter,
            self.gs.max_double_counter, 
            750, self.background_rect.top + 15,
                150, 19 )
        
        

        #### PAUSE MENU METHODS ####

        
    def create_bar(self, screen, param, max_param, x, y,
                   long, wide):

        
        self.bar_calc = int((param / max_param) * long)
        
        self.edge = pygame.Rect(x, y, long, wide)
        self.bar = pygame.Rect(x, y, self.bar_calc, wide)

        if self.bar_calc < long * 0.10:
            self.bar_color = red

        elif self.bar_calc >= long * 0.10 and self.bar_calc < long * 0.35:
            self.bar_color = orange

        elif self.bar_calc >= long * 0.35 and self.bar_calc < long * 0.5:
            self.bar_color = yellow

        else:
            self.bar_color = green
        pygame.draw.rect(screen, white, self.edge, 1)
        pygame.draw.rect(screen, self.bar_color, self.bar)

    def show_text(self, screen, font, text, color, size, x, y):
        style = pygame.font.Font(font, size)
        surface = style.render(text, True, color).convert_alpha()
        rectangle = surface.get_rect()
        rectangle.center = (x, y)
        screen.blit(surface, rectangle)

        ####INTRO METHODS####

    def _show_logo(self):
        """muestra el logo con un fade in en pantalla """
        self.logo.set_alpha(self.logo_alpha)
        self.screen.blit(self.logo,self.logo_rect)
        self.logo_alpha += 2

    def _limit_alpha(self):
        """impide que el alpha de logo supere los 255"""
        if self.logo_alpha >= 255:
            self.logo_alpha = 255

    def _intro_text(self):
        """muestra PRESENTS al final del fundido del logo"""
        if self.logo_alpha >= 200:
            self.show_text(
                self.screen,comic,"PRESENTS:", black, 50,
                self.screen_rect.centerx,window_heigh - 100)
            

class Instructions():
    def __init__(self):
        self.index = 0
        self.image = [
            pygame.image.load(
            f'images/instructions/instructions_{i}.png'
            ).convert_alpha() for i in range (3)]
        
    def blit_me(self, surface):
        surface.blit(self.image[self.index], (0,0))
       
            

    






