import pygame
import random
from scripts.powerup import Powerup
import os

class atkBoost(Powerup):
    atkBoost = pygame.image.load(os.path.join('assets', 'sprites', 'AtkBoost.png'))

    def __init__(self,AttackBoost):
        super().__init__(X = 0, Y = 0)
        self.AttackBoost = AttackBoost
        self.X = 1050
        self.Y = random.randint(50,450)
        self.Speed = -1

        self.width = 60
        self.height = 48

    def draw(self, win):
        self.X += self.Speed
        win.blit(self.atkBoost, (self.X, self.Y))