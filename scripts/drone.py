import pygame as pg


class Drone(pg.sprite.Sprite):
    def __init__(self, x, y):

        self.x_vel = 0
        self.y_vel = 0
