import pygame as pg
from scripts.data import setup,tools
 
class Button:
    def __init__(self, rect, command, picture = None):
        self.picture = None
        if picture != None:
            self.picture = setup.GFX[picture]
            self.picture_pressed = setup.GFX[picture+'-pressed']
        self.rect = pg.Rect(rect)
        self.image = pg.Surface(self.rect.size).convert()
        self.image.fill((255,255,255))
        self.function = command
        self.pressed = False
        self.timer = 0
 
    def get_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            self.on_click(event)
 
    def on_click(self, event):
        if self.rect.collidepoint(event.pos):
            self.function()
            self.pressed = True
 
    def draw(self, surf):
        if self.picture != None and self.pressed == False:
            surf.blit(self.picture, self.rect)
        elif self.picture != None and self.pressed == True:
            surf.blit(self.picture_pressed, self.rect)
        else:
            surf.blit(self.image, self.rect)
        if "mouse" not in tools.keyPressed and self.pressed == True:
            self.pressed = False
