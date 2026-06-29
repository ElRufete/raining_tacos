import sys
import pygame
from settings import *
from tacos import *
from player import Player
from spawner import Spawner
from status import Game_Status
from sound import Music
from ui import UI, Instructions
from debug import Debug

class RainingTacos:
    """Clase general para gestionar recursos y comportamientos del juego"""

    def __init__(self):
        """inicializa el juego y crea recursos"""
        pygame.init()
        
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(
            (window_width,window_heigh))
        self.screen_rect = self.screen.get_rect()
        self.screen.fill(black)
        self.background = pygame.image.load(
            'images/Fondos/tacos_bg1.png').convert_alpha() 
        self.intro_bg = pygame.Surface((
                window_width, window_heigh)).convert_alpha()
        self.intro_bg.fill(orange)
        self.black_bg = pygame.Surface(
            (window_width,window_heigh)).convert_alpha()
        self.black_bg.fill(black)
        self.sky = pygame.Surface((
                window_width, window_heigh)).convert_alpha()
        self.sky.fill(blue)
        self.player = Player(self)
        self.gs = Game_Status()
        self.spawner = Spawner(self)
        self.inst = Instructions()
        self.ui = UI(self)
        self.music = Music('music/menu_music.ogg')
        self.debug = Debug(self)
        
        self.gs.check_saved_highscore()
        
    def run_game(self):
            """Maneja el bucle principal del juego"""
            while True:
                self.clock.tick(fps)
                self._check_events()  
                self._check_collisions()
                self._update_screen()
                self._gameover()
                
                
                
                
    def _gameover(self):
        """Prepara el menú de game over 
        si el jugador se queda sin vidas"""
        if self.gs.lives <= 0:
            self.music.stop_music()
            if self.gs.score > self.gs.high_score:
                self.gs.high_score = self.gs.score
            self.gs.save_high_score()
            self._clear_groups()
            self.gs.status = "game over"
            
    def _update_screen(self):
        """Actualiza la pantalla en cada vuelta del bucle"""

        if self.gs.status == "intro":
            self.screen.blit(self.intro_bg, (0,0))
            for taco in intro_tacos:
                if taco.rect.bottom >= (window_heigh - 40):
                    taco.kill()
                    self.music.play_music()
                    self.gs.status = "menu"
            self.spawner.update()
            intro_tacos.update()

        if self.gs.status == "menu":
            self.screen.blit(self.sky, (0,0))
            bg_clouds.draw(self.screen)
            clouds.draw(self.screen)
            bg_clouds.update()
            clouds.update()
            if self.ui.play_bt.click():
                self.music = Music('music/raining_tacos.ogg')
                self.music.play_music()
                players.add(self.player)
                self.spawner.drop_clouds = True
                clouds.empty()
                bg_clouds.empty()
                self.gs.status = "gameplay"
            if self.ui.quit_bt.click():
                sys.exit()
            if self.ui.htp_bt.click():
                self.gs.status = "instructions"
            self.spawner.update()

        if self.gs.status == "instructions":
            self.inst.blit_me(self.screen)
            if self.ui.menu_bt.click():
                self.gs.status = "menu"
            if self.ui.r_arrow_bt.click() and self.inst.index < 2:
                self.inst.index += 1
            if self.ui.l_arrow_bt.click() and self.inst.index > 0:
                self.inst.index -= 1
            if self.inst.index == 1:
                if self.ui.hidden_bt.click():
                    if self.gs.jumpscare_index < 10:
                        self.gs.hello_index += self.gs.hello_increase
                        self.gs.hello_increase *= -1
                        self.gs.jumpscare_index += 1
                        if self.gs.jumpscare_index != 10:
                            hello[self.gs.hello_index].play()
                    if self.gs.jumpscare_index >= 10:
                        self.music.stop_music()
                        scream.play()
                        self.spawner.spawn_balloon_boy()
                        self.gs.status = "jumpscare"
                        self.gs.jumpscare_index = 0
                        self.gs.hello_increase = 1
                        self.gs.hello_index = 0
                        self.inst.index = 0
                        

        if self.gs.status == "jumpscare":
            self.screen.blit(self.black_bg,(0,0))
            effects.update()
            if self.spawner.balloon_boy.animation_counter >= 120:
                self.gs.status = "game over"
            
        if self.gs.status == "gameplay":
            self.screen.blit(self.background,(0,0))
            self._update_groups()
            self.spawner.update()
            self.gs.manage_double()

        if self.gs.status == "pause":
            self.screen.blit(self.background,(0,0))
            if self.ui.resume_bt.click():
                self.music.resume_music()
                self.gs.status = "gameplay"
            if self.ui.quit_bt.click():
                sys.exit()
            if self.ui.restart_bt.click():
                self.restart_gameplay()
            if self.ui.menu_bt.click():
                self._go_menu()


        if self.gs.status == "game over":
            if self.ui.quit_bt.click():
                sys.exit()
            if self.ui.play_again_bt.click():
                self.music = Music('music/raining_tacos.ogg')
                self.restart_gameplay()
            if self.ui.menu_bt.click():
                self._go_menu()
          
        self.gs.update()
        self._draw_sprites()
        self.ui.blit_me()
        intro_tacos.draw(self.screen)
        pygame.display.flip()        

    def _check_events(self):
        """Busca eventos de teclado y ratón."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                #comprueba si hay eventos de pulsación de tecla.
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                #comprueba si hay eventos de pulsación de tecla.
                self._check_keyup_events(event)

        
    def _check_keydown_events(self, event):
        pass


    def _check_keyup_events(self, event):
        if event.key == pygame.K_q:
            sys.exit()

        if event.key == pygame.K_ESCAPE:
            if self.gs.status == "gameplay":
                self.music.pause_music()
                self.gs.status = "pause"


    def _check_collisions(self):
        """comprueba si los sprites chocan entre sí"""
        collision = pygame.sprite.spritecollide(
            self.player, tacos, True)
        collision_bunshin = pygame.sprite.groupcollide(
            bunshins, tacos, False, True)
        collision_clancy = pygame.sprite.groupcollide(
            clancies, tacos, False, True)
        collision_goose_icon = pygame.sprite.spritecollide(
            self.player, goose_icons, True)
        collision_heart = pygame.sprite.spritecollide(
            self.player, heart_icons, True)
        collision_pepper = pygame.sprite.spritecollide(
            self.player, pepper_icons, True)
        collision_bunshin_icon = pygame.sprite.spritecollide(
            self.player, bunshin_icons, True)
        collision_goose = pygame.sprite.groupcollide(
            geese, tacos, False, True)
        collision_limon_icon = pygame.sprite.spritecollide(
            self.player, limon_icons, True)
        collision_clancy_icon = pygame.sprite.spritecollide(
            self.player, clancy_icons, True)
        collision_double_icon = pygame.sprite.spritecollide(
            self.player, double_icons, True)


        if collision_bunshin:
            for bunshin in collision_bunshin:
                if bunshin in bunshins:
                    bunshin.get_crumbs()
                    if self.player.spice < self.player.max_spice:
                            self.player.spice += 8
                    self.gs.score += 1
                    nom.play()

        if collision_clancy:
            for clancy in collision_clancy:
                if clancy in clancies:
                    clancy.get_crumbs()
            self.gs.score +=1
            shark.play()
        
        if collision:

            if self.gs.double:
                self.gs.score += 2
            else:
                self.gs.score += 1

            if self.player.spice < self.player.max_spice: 
                self.player.spice += 8
            self.player.get_crumbs()
            nom.play()

            
        if collision_goose_icon:
            self.player.get_goose()
            
        if collision_goose:
            for goose in collision_goose:
                if goose in geese:
                    goose.get_crumbs()
                    self.player.spice += 3
                    self.gs.score += 1
                    quack.play()

        if collision_heart:
            if self.gs.lives < 10:
                self.gs.lives += 1
                life_up.play()
        
        if collision_pepper:
            self.player.spice += 100
            life_up.play()

        if collision_bunshin_icon:
            if len(bunshins) <= 0:
                self.player.get_bunshin()
            else:
                for bunshin in bunshins:
                    bunshin.renew()
            
        if collision_limon_icon:
            for taco in tacos:
                taco.islimon = True
            limon_sounds[0].play()

        if collision_clancy_icon:
            if not self.spawner.clancy_active:
                self.spawner.clancy_active = True
            else: self.spawner.clancy_counter = self.spawner.max_clancy_counter
            life_up.play()

        if collision_double_icon:
            if not self.gs.double:
                self.gs.double = True
            else: self.gs.double_counter = self.gs.max_double_counter
            life_up.play()


    def _update_groups(self):
        """actualiza el estado de los Sprites en cada bucle"""
        tacos.update()
        effects.update()
        players.update()
        geese.update()
        bunshins.update(self.player)
        clancies.update()
        goose_icons.update()
        bunshin_icons.update()
        heart_icons.update()
        limon_icons.update()
        limons.update()
        clancy_icons.update()
        pepper_icons.update()
        double_icons.update()
        

    def _draw_sprites(self):
        """Dibuja los sprites en la pantalla"""
        tacos.draw(self.screen)
        bunshins.draw(self.screen)
        players.draw(self.screen)
        geese.draw(self.screen)
        clancies.draw(self.screen)
        goose_icons.draw(self.screen)
        bunshin_icons.draw(self.screen)
        heart_icons.draw(self.screen)
        limon_icons.draw(self.screen)
        clancy_icons.draw(self.screen)
        pepper_icons.draw(self.screen)  
        double_icons.draw(self.screen)
        limons.draw(self.screen) 
        effects.draw(self.screen)  


    def restart_gameplay(self):
        """reinicia la partida"""
        self._reset_stats()
        self._clear_groups()
        self._recall_player()
        self.music.play_music()
        self.gs.status = "gameplay"


    def _clear_groups(self):
        """Elimina todos los sprites"""
        tacos.empty()
        bunshins.empty()
        players.empty()
        geese.empty()
        clancies.empty()
        goose_icons.empty()
        bunshin_icons.empty()
        heart_icons.empty()
        limon_icons.empty()
        clancy_icons.empty()
        pepper_icons.empty()
        double_icons.empty()
        limons.empty()
        effects.empty()


    def _reset_stats(self):
        """Devuelve las estadísticas al estado inicial"""
        self.gs.lives = self.gs.init_lives
        self.player.spice = 0
        self.spawner.clancy_counter = 0
        self.spawner.clancy_active = False
        for bunshin in bunshins:
            bunshin.counter = 0
        self.gs.score = 0
        self.gs.double = False
        self.gs.double_counter = self.gs.max_double_counter
        self.spawner.n_taco_spawner = 0
        self.spawner.b_taco_spawner = 0
        self.spawner.s_taco_spawner = 0
        self.spawner.m_taco_spawner = 0
        self.spawner.spawn_increase = self.spawner.init_spawn_increase
        


    def _recall_player(self):
        """Vuelve a crear la instancia de jugador"""
        self.player = Player(self)
        self.ui = UI(self)
        players.add(self.player)

    def _go_menu(self):
        """lleva al jugador de vuelta al menú principal"""
        self._reset_stats()
        self._clear_groups()
        self.music.music_file = 'music/menu_music.ogg'
        self.music.play_music()
        self.gs.status = "menu"
        

if __name__ == '__main__':

    rt_game = RainingTacos()
   
    rt_game.run_game()
    
    
    