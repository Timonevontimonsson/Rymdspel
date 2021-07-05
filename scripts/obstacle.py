#! python3

from scripts.creature import Creature
import pygame
import os
import random


class Obstacle(Creature):
    asteroid = pygame.image.load(os.path.join('assets', 'sprites', 'Asteroid.png'))

    def __init__(self):
        self.Health = 20
        self.X = 1100
        self.Y = random.randint(10,490)

        self.width = 32
        self.height = 32
        self.rect = pygame.Rect(self.X, self.Y, 50, 50)

    def draw(self, win):
         win.blit(self.asteroid, (self.X, self.Y))

    def moove(self, Speed):
        self.X += -Speed
        self.rect.x -= Speed

       

   

   

