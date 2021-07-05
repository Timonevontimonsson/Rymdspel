from scripts.enemy import Enemy
from scripts.projectile import Projectile
import os
import pygame
import random


class Explorer(Enemy):
    explorer = pygame.image.load(os.path.join('assets', 'sprites', 'Explorer.png'))
    def __init__(self):
        self.X = 1150
        self.Y = random.randint(50, 450)
        self.Health = 15
        self.Speed = 1
        
        self.width = 32
        self.height = 32

        self.giveScore = 500
        
        
        self.n = 0
        self.nSpeed = 1

        self.timeSinceLastShot = 0

    def draw(self, win):
        self.X -= self.Speed
        win.blit(self.explorer, (self.X, self.Y))

        self.Y += self.nSpeed
        self.n += self.nSpeed
        if self.n == 48:
            self.nSpeed *= -1
        elif self.n == 0:
            self.nSpeed *= -1

    def shoot(self, dt, player):
        self.timeSinceLastShot += dt
        if self.timeSinceLastShot > 1700:
            self.timeSinceLastShot = 0
            player.enemyProjektiler.append(Projectile(self.X-8, self.Y+5 ,-4, pygame.image.load(os.path.join('assets', 'sprites', 'RedLaser.png')),12,5))


