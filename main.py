# Elias Hedberg
# Python 3
import pygame
from pygame.locals import *
import os
import configparser
import random
import math


debug = False
config = configparser.ConfigParser()
       
pygame.init()
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (45,20) 
win_width = 1920
win_height = 1080
game = pygame.display.set_mode((win_width, win_height)) 


ADDPREY = pygame.USEREVENT + 1 # Eventet som sker då en fiende läggs till
pygame.time.set_timer(ADDPREY, 1500) # Hur stor delay (ms) tills nästa fiende spawnar

def SetRandomPath():
    return (random.randint(0,win_width), random.randint(0,win_height))

def Distance(obj1: tuple, obj2: tuple):
    return math.sqrt( (obj1(0) - obj2(0)) ** 2 + (obj1(1) - obj2(1) ** 2) )

class Prey(pygame.sprite.Sprite):
    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self)
        config.read("prey.ini")

        self.image = pygame.image.load("assets/prey.png")
        self.rect = self.image.get_rect()
        self.rect.center = (600, 600)

        self.health = config.getint("prey", "HEALTH")
        self.size = config.getint("prey", "SIZE")
        self.speed = config.getint("prey", "SPEED")

        self.goal = None

    def update(self):
        self.DetermineAction()
        self.FindPath()

    def DetermineAction(self):
        if self.goal == None:
            self.Search()
        elif self.goal == "roam":
            if self.Search == None:
                SetRandomPath()
            else:
                self.goal = self.Search()


    def Search(self):
        found = None
        return found

    def FindPath(self):
        pass
    
    


def redrawGameWindow():
    pygame.draw.rect(game, (0,0,0),(0,0,win_width,win_height))
    all_sprites.update()
    all_sprites.draw(game) # Målar spriten


clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
prey = pygame.sprite.Group()

run = True
while run:  # Mainloop every tick
    clock.tick(60)  # clock(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif (event.type == ADDPREY):
            new_prey = Prey()
            prey.add(new_prey)
            all_sprites.add(new_prey)

        redrawGameWindow()


pygame.quit()

