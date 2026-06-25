import pygame
from pathlib import Path
import json

class Game_Status():
    def __init__(self):
        self.max_lives = 10
        self.init_lives = 5
        self.lives = self.init_lives
        self.score = 0
        self.high_score = 0
        self.path = Path('high_score.json')
        self.status = "intro"
        self.double = False
        self.max_double_counter = 480
        self.double_counter = self.max_double_counter
        self.hello_index = 0
        self.hello_increase = 1
        self.jumpscare_index = 0

    def update(self):
        if self.lives >= self.max_lives:
            self.lives = self.max_lives

    def check_saved_highscore(self):
        if self.path.exists():
            self.load_high_score()
        else: 
            self.high_score = 0    
    
    def load_high_score(self):

        contents = self.path.read_text()
        self.high_score = json.loads(contents)

    def save_high_score(self):

        contents = json.dumps(self.high_score)
        self.path.write_text(contents) 

    def manage_double(self):
        if self.double:
            self.double_counter -= 1

        if self.double_counter <= 0:
            self.double_counter = self.max_double_counter
            self.double = False
            

        
        


