# Elias Hedberg
# Python 3
import pygame
from pygame.locals import *
import os
import configparser
import random
import math
import numpy


debug = True
config = configparser.ConfigParser()
       
pygame.init()
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (45,20) 
win_width = 1920
win_height = 1080
game = pygame.display.set_mode((win_width, win_height)) 


ADDPREY = pygame.USEREVENT + 1 # Event
PREGNANCY = pygame.event.Event(ADDPREY)
#pygame.time.set_timer(ADDPREY, 1500) # delay

ADDFOOD = pygame.USEREVENT + 2 # Event
pygame.time.set_timer(ADDFOOD, 1500) # delay
STARTFOOD = pygame.event.Event(ADDFOOD)
#pygame.time.set_timer(ADDPREY, 1500) # delay

REMOVEHEALTH = pygame.USEREVENT + 3 # Event
pygame.time.set_timer(REMOVEHEALTH, 3000) # delay

def SetRandomPath(pos):
    path = (random.randint(pos[0] - win_width/10, pos[0] + win_width/10), random.randint(pos[1] - win_height/10, pos[1] + win_height/10))
    if path[0] > win_width or path[0] < 0 or path[1] > win_height or path[1] < 0:
        SetRandomPath(pos)
    else:
        return path

def Distance(obj1: tuple, obj2: tuple):
    return math.sqrt( abs(obj1[0] - obj2[0]) ** 2 + abs(obj1[1] - obj2[1] ** 2) )

def in_circle(x_char, y_char, radius, x_food, y_food):
    square_dist = (x_char - x_food) ** 2 + (y_char - y_food) ** 2
    return square_dist <= radius ** 2

class Prey(pygame.sprite.Sprite):
    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self)
        config.read("prey.ini")

        self.health = config.getint("prey", "HEALTH")
        self.size = config.getint("prey", "SIZE")
        self.speed = config.getint("prey", "SPEED")
        self.vision = config.getint("prey", "VISION")
        self.goal = None

        self.image = pygame.transform.scale(pygame.image.load("assets/prey.png"), (self.size,self.size))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0,win_width), random.randint(0,win_height))
        self.exact_pos = (float(self.rect.centerx), float(self.rect.centery))
        
        self.pregnancycounter = 0

    def update(self):
        self.DetermineAction()
        self.FindPath()
        self.rect.center = (round(self.exact_pos[0]), round(self.exact_pos[1]))
        if self.health >= 40:
            self.pregnancycounter += 1
        if self.pregnancycounter / 60 == 15:
            self.pregnancycounter = 0
            pygame.event.post(PREGNANCY)
        

    def DetermineAction(self):
        if self.goal == None:
            self.goal = self.Search()
            if self.goal == None:
                self.goal = SetRandomPath(self.rect.center)
        else:
            self.Walk()

    def Search(self):
        for plant in food:
            if in_circle(self.rect.centerx, self.rect.centery, self.vision, plant.rect.centerx, plant.rect.centery):
                return (plant.rect.centerx, plant.rect.centery)
        return None

    def FindPath(self):
        pass

    def Walk(self):
        vector = tuple(numpy.subtract(self.rect.center, self.goal))
        hyp = math.sqrt(vector[0]*vector[0] + vector[1]*vector[1])
        if hyp < 5:
            self.goal = None
        vectorx = (vector[0]/hyp * self.speed)
        vectory = (vector[1]/hyp * self.speed)
        
        self.exact_pos = (self.rect.centerx - vectorx, self.rect.centery - vectory)


class Food(pygame.sprite.Sprite):
    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self)
        config.read("food.ini")

        self.size = config.getint("food", "SIZE")
        self.nutrient = config.getint("food", "NUTRIENT")

        self.image = pygame.transform.scale(pygame.image.load("assets/food.png"), (self.size,self.size))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0,win_width), random.randint(0,win_height))


def redrawGameWindow():
    pygame.draw.rect(game, (0,102,0),(0,0,win_width,win_height))
    all_sprites.update()
    all_sprites.draw(game) # Målar spriten

    if debug:
        for individual in prey:
            pygame.draw.circle(game, (255, 255, 255, 40), individual.rect.center, individual.vision, 2)
            if individual.goal != None:
                pygame.draw.line(game, (255, 255, 255), individual.rect.center, individual.goal, 3)

    pygame.display.update()


clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
prey = pygame.sprite.Group()
food = pygame.sprite.Group()

run = True

pygame.event.post(PREGNANCY)

for i in range(10):
    pygame.event.post(STARTFOOD)

while run:  # Mainloop every tick
    clock.tick(60)  # clock(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif (event.type == ADDPREY):
            new_prey = Prey()
            prey.add(new_prey)
            all_sprites.add(new_prey)

        elif (event.type == ADDFOOD):
            new_food = Food()
            food.add(new_food)
            all_sprites.add(new_food)

        elif (event.type == REMOVEHEALTH):
            for individual in prey:
                individual.health -= 20
                if individual.health <= 0:
                    individual.kill()

    for individual in prey:
        for fruit in food:
            if pygame.sprite.collide_rect(individual, fruit):
                individual.health += fruit.nutrient
                if individual.health > 100:
                    individual.health = 100
                fruit.kill()
                 

    redrawGameWindow()


pygame.quit()

