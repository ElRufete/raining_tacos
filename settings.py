import pygame


score = 0

#ventana y reloj#
window_width = 940
window_heigh = 700

fps = 60


#colores
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (80, 140, 255)
cyan = (0, 255, 255)
yellow = (255, 255, 0)
orange = (255, 115, 0)
chris_color = (50, 0, 110)
pink = (255, 120, 120)

#fuentes

comic = pygame.font.match_font("comic sans")

#SONIDOS

pygame.mixer.init()

nom = pygame.mixer.Sound("Sounds/nom.wav")
taco_fall = pygame.mixer.Sound("Sounds/taco_fall.wav")
shark = pygame.mixer.Sound("Sounds/tiburon.wav")
goose_sound = pygame.mixer.Sound("Sounds/get_shark.wav")
life_up = pygame.mixer.Sound("Sounds/live_up.wav")
speed_up = pygame.mixer.Sound("Sounds/speedup.wav")
jutsu = pygame.mixer.Sound("Sounds/bunshin_buff.ogg")
nani = pygame.mixer.Sound("Sounds/nani.ogg")
quack = pygame.mixer.Sound("Sounds/quack.ogg")
glass = pygame.mixer.Sound("Sounds/glass.ogg")
bunshin_extend = pygame.mixer.Sound("Sounds/bunshin_extend.wav")
siu = pygame.mixer.Sound("Sounds/siu.ogg")
limon_sounds = [
    pygame.mixer.Sound("Sounds/limon1.ogg"),
    pygame.mixer.Sound("Sounds/limon2.ogg"),]
taco_drop = pygame.mixer.Sound("Sounds/drop_taco.wav")
hello = [pygame.mixer.Sound('Sounds/_hello.ogg'),
         pygame.mixer.Sound('Sounds/_hi.ogg')]
scream = pygame.mixer.Sound('Sounds/_jumpscare.ogg')


#GRUPOS

tacos = pygame.sprite.Group()
effects = pygame.sprite.Group()
geese = pygame.sprite.Group()
players = pygame.sprite.Group()
heads = pygame.sprite.Group()
bunshins = pygame.sprite.Group()
clancies = pygame.sprite.Group()
goose_icons = pygame.sprite.Group()
heart_icons = pygame.sprite.Group()
bunshin_icons = pygame.sprite.Group()
limon_icons = pygame.sprite.Group()
limons = pygame.sprite.Group()
clancy_icons = pygame.sprite.Group()
pepper_icons = pygame.sprite.Group()
double_icons = pygame.sprite.Group()
clouds = pygame.sprite.Group()
bg_clouds = pygame.sprite.Group()
intro_tacos = pygame.sprite.Group()



