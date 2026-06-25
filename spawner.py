import pygame
from settings import *
from tacos import *
from powerups import *
from clouds import Cloud, BackCloud

class Spawner():
    """clase que maneja los tiempos de spawn de tacos, powerups y nubes"""
    def __init__ (self, rt_game):

        self.player = rt_game.player
        self.gs = rt_game.gs
        self.screen_rect = rt_game.screen_rect

        #DIFICULTAD

        self.init_spawn_increase = 3
        self.spawn_increase = self.init_spawn_increase
        
        # LISTA DE TACOS

        self.taco_list = {
            'normal' : {'name': NTaco, 'threshold': 540, 
                         'counter': 0, 'min_score': 0},
            'balloon' : {'name': BTaco, 'threshold': 1400, 
                         'counter': 0, 'min_score': 3},
            'speedy' : {'name': STaco, 'threshold': 2000, 
                         'counter': 0, 'min_score': 9},
            'meditaco' : {'name': MTaco, 'threshold': 2500, 
                         'counter': 0, 'min_score': 14},
        }

        #Ruleta de iconos y condiciones de spawneo 

        self.roulette_range = 40_000  
        self.icon_roulette = [
            {'cls': HeartIcon, 'chance': (1,50), 
            'cond' : lambda gs: gs.lives < 10 and len(heart_icons) == 0},
            {'cls': GooseIcon, 'chance': (60,110), 
            'cond' : lambda gs: gs.score >= 15 and len(goose_icons) == 0},
            {'cls': BunshinIcon, 'chance': (110,130), 
            'cond' : lambda gs: gs.score >= 70 and len(bunshin_icons) == 0 
            and len(bunshins) == 0},
            {'cls': ClancyIcon, 'chance': (140,155), 
            'cond' : lambda gs: gs.score >= 100 and len(clancy_icons) == 0 
            and not self.clancy_active},
            {'cls': PepperIcon, 'chance': (155,190), 
            'cond' : lambda gs: gs.score >= 70 and len(pepper_icons) == 0},
            {'cls': DoubleIcon, 'chance': (190,205), 
            'cond' : lambda gs: gs.score >= 100 and len(double_icons) == 0 
            and not gs.double},
            {'cls': LimonIcon, 'chance': (23716,23716), 
            'cond' : lambda gs: gs.score >= 100 and len(limon_icons) == 0},  
        ]
       
        
        self.drop_clouds = True
        self.clancy_active = False
        self.max_clancy_counter = 540
        self.clancy_counter = self.max_clancy_counter
        self.intro_counter = 0

    def update(self):

        if self.gs.status == "intro":
            self.intro_counter += 1
            if self.intro_counter == 240:
                self.i_taco = IntroTaco()
                intro_tacos.add(self.i_taco)
                goose_sound.play()


        if self.gs.status == "menu":
            self._drop_clouds()
            self._renew_clouds()

            
        if self.gs.status == "gameplay":            
            self._spawn_taco()
            self._spawn_clancy()
            self._increase_difficulty()
            self._roll_roulette()

    def spawn_balloon_boy(self):
        self.balloon_boy = BalloonBoy(self)
        effects.add(self.balloon_boy)
        
    def _spawn_taco(self):
         """genera tacos cada cierto tiempo"""

         for name, taco in self.taco_list.items():
              if self.gs.score >= taco['min_score']:
                   taco['counter'] += self.spawn_increase
                   if taco['counter'] >= taco['threshold']:
                        tacos.add(taco['name'](self))
                        taco['counter'] = 0



    def _spawn_clancy(self):
        """genera un clancy cuando un taco está a punto de caer"""
        if self.clancy_active:
            self.clancy_counter -= 1
            for taco in tacos:
                if taco.rect.bottom >= (window_heigh - 15):
                    if len(clancies) < 1:
                        self.clancy = Clancy(taco.rect.centerx)
                        clancies.add(self.clancy)
        if self.clancy_counter <= 0:
            self.clancy_active = False
            self.clancy_counter = self.max_clancy_counter


    def _increase_difficulty(self):
        """Aumenta la frecuencia de spawn al subir la puntuación"""
        if self.gs.score >= 40 and self.gs.score < 70:
            self.spawn_increase = 4

        elif self.gs.score >= 70 and self.gs.score < 110:
            self.spawn_increase = 5

        elif self.gs.score >= 110 and self.gs.score < 170:
            self.spawn_increase = 7

        elif self.gs.score >= 170:
            self.spawn_increase = 9

            
        ###############################   ICON ROULETTE    ########################

    def _roll_roulette(self):
        """Genera power-ups de forma aleatoria"""
        roll = randint(0,self.roulette_range)
        for rule in self.icon_roulette:
            if rule['chance'][0] <= roll <= rule['chance'][1]:
                if rule['cond'](self.gs):
                    icon = rule['cls'](self)

                    if type(icon) is HeartIcon:
                        heart_icons.add(icon)
                    elif type(icon) is GooseIcon:
                        goose_icons.add(icon)
                    elif type(icon) is BunshinIcon:
                        bunshin_icons.add(icon)
                    elif type(icon) is ClancyIcon:
                        clancy_icons.add(icon)
                    elif type(icon) is PepperIcon:
                        pepper_icons.add(icon)
                    elif type(icon) is DoubleIcon:
                        double_icons.add(icon)
                    elif type(icon) is LimonIcon:
                        limon_icons.add(icon)
        self._improve_droprate()


    def _improve_droprate(self):
        """Aumenta la probabilidad de obtener 
        power-ups al aumentar la puntuación"""
        if self.gs.score >= 100:
            self.roulette_range = 35_000
        if self.gs.score >= 150:
            self.roulette_range = 30_000


    ###### MENU METHODS ########


    def _drop_clouds(self):
        """dibuja las nubes en el cielo"""
        if self.drop_clouds:
                    self.ypos_front = 100
                    self.ypos_back = 250
                    for i in range (3):
                        self.cloud = Cloud(self.ypos_front)
                        clouds.add(self.cloud)
                        self.ypos_front += self.cloud.rect.height + 100
                    for i in range (2):
                        self.bg_cloud = BackCloud(self.ypos_back)
                        bg_clouds.add(self.bg_cloud)
                        self.ypos_back += self.bg_cloud.rect.height + 250
                    self.drop_clouds = False

    def _renew_clouds(self):
        """crea una nueva nube cuando alguna llega arriba"""
        if len(clouds) < 3:
            self.cloud = Cloud(window_heigh)
            clouds.add(self.cloud)
        if len(bg_clouds) < 2:
            self.bg_cloud = BackCloud(window_heigh)
            bg_clouds.add(self.bg_cloud)


   








    