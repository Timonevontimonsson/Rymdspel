import pygame as pg
from scripts.data import setup
from scripts.data import constant as c

class Shield(pg.sprite.Sprite):
    def __init__(self, x, y, amount):
        super(Shield, self).__init__()
        self.sprite_sheet = setup.GFX['Shield']
        self.setup_frames()
        self.state = c.START
        self.frame_index = 0
        self.animation_timer = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.right = 0
        self.rect.y = 0
        self.xPos = x
        self.yPos = y
        self.current_shield = amount
        self.maximum_shield = amount
        self.name = 'shield'
        self.cooldown_timer = 2000
        self.lasting_timer = 10000

    def setup_frames(self):
        self.frames = []
        
        self.frames.append(
            self.get_image(0,0,40,40))

    def get_image(self, x, y, width, height):
        """Get the image frames from the sprite sheet"""

        image = pg.Surface([width, height]).convert()
        rect = image.get_rect()

        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        transColor = image.get_at((0,0))
        image.set_colorkey(transColor)
        


        image = pg.transform.scale(image,
                                   (int(rect.width*1),
                                    int(rect.height*1)))
        return image

    def update(self, player):
        """Updates laser behavior"""
        self.current_time = player.current_time
        self.player = player
        self.handle_state()

    def handle_state(self):
        """Handles behavior based on state"""
        if self.state == c.START:
            self.update_shield()
            self.animation()
            
        elif self.state == c.HIT:
            self.animation()

    def update_shield(self):
        self.rect.x = self.player.rect.x + self.xPos
        self.rect.y = self.player.rect.bottom + self.yPos


    def animation(self):
        if self.state == c.START:
            if (self.current_time - self.animation_timer) > 400:
                if self.frame_index < 0:
                    self.frame_index += 0
                else:
                    self.frame_index = 0
                self.animation_timer = self.current_time
                self.image = self.frames[self.frame_index]
        elif self.state == c.HIT:
            if (self.current_time - self.animation_timer)  >  1000:
                if self.frame_index < 0:
                    print(self.frame_index)
                    self.frame_index += 0
                    self.image = self.frames[self.frame_index]
                    self.animation_timer = self.current_time
                else:
                    self.kill()