#! python3
import pygame

class Creature():
    def __init__(self, Health, X, Y):
        self.Health = Health
        self.X = X
        self.Y = Y

    def get_rect(self):
         return pygame.Rect(self.X, self.Y, self.width, self.height)
        