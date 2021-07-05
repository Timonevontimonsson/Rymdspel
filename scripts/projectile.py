import pygame
import os

class Projectile:
    

    def __init__(self, X, Y,Speed, img, width, height):
        self.X = X
        self.Y = Y
        self.Speed = Speed
        self.Damage = 5
        self.width = width
        self.height = height
        self.laser = img


    def draw(self, win):
        self.X += self.Speed
        win.blit(self.laser, (self.X, self.Y))

    def get_rect(self):
         return pygame.Rect(self.X, self.Y, self.width, self.height)