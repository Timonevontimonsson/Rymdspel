from scripts.powerup import Powerup
import random
import os
import pygame

class Heart(Powerup):
    heart = pygame.image.load(os.path.join('assets', 'sprites', 'Heart.png'))

    def __init__(self,Healing):
        super().__init__(X = 0, Y = 0)
        self.Healing = Healing
        self.X = 1050
        self.Y = random.randint(50,450)
        self.Speed = -1

        self.width = 60
        self.height = 48

    def draw(self, win):
        self.X += self.Speed
        win.blit(self.heart, (self.X, self.Y))

