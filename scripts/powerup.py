
import pygame as pg
from scripts.data import constant as c
from scripts.data import setup
from scripts import score
import random

class Powerup(pg.sprite.Sprite):
    #basklass för att powerups
    def __init(self, x, y):
        super(Powerup, self).__init__()

    def setup_powerup(self, x, y, name, setup_frames):
        #en seoarat setup funktion som tillåter en att lägga in en annan setup_frames metod beroende på vilken powerup det är
        self.sprite_sheet = setup.GFX['RedLaser']
        self.frames = []
        self.frame_index = 5
        setup_frames()
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = y
        self.y_vel = 0
        self.x_vel = -1
        self.animate_timer = 0
        self.name = name
        

    def get_image(self, x, y, width, height):
        """Get the image frames from the sprite sheet"""

        image = pg.Surface([width, height]).convert()
        rect = image.get_rect()

        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(c.BLACK)


        image = pg.transform.scale(image,
                                   (int(rect.width*c.SIZE_MULTIPLIER),
                                    int(rect.height*c.SIZE_MULTIPLIER)))
        return image

    def update(self, game_info, *args):
        self.current_time = game_info[c.CURRENT_TIME]
        self.hande_state()

    def hande_state(self):
        pass

    def moving(self):
        self.x_vel = -3

class Heart(pg.sprite.Sprite):
    def __init__(self, x, y):
        super(Heart, self).__init__()
        self.sprite_sheet = setup.GFX['Heart']
        self.setup_frames()
        self.x_vel = -1
        self.y_vel = 0
        self.state = c.START
        self.frame_index = 0
        self.animation_timer = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.right = x
        self.rect.y = y
        self.name = c.HEART_LVL_1

    def setup_frames(self):
        self.frames = []

        self.frames.append(
            self.get_image(0, 0, 50,50))

    def get_image(self, x, y, width, height):
        """Get the image frames from the sprite sheet"""

        image = pg.Surface([width, height]).convert()
        rect = image.get_rect()

        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        transColor = image.get_at((0,0))
        image.set_colorkey(transColor)
        


        image = pg.transform.scale(image,
                                   (int(rect.width*0.3),
                                    int(rect.height*0.3)))
        return image

    def update(self, game_info):
        """Updates laser behavior"""
        self.current_time = game_info[c.CURRENT_TIME]
        self.handle_state()

    def handle_state(self):
        """Handles behavior based on state"""
        if self.state == c.START:
            self.animation()
            
        elif self.state == c.HIT:
            self.animation()

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

class Laser(pg.sprite.Sprite):
    def __init__(self, x, y,dmg, name = c.LASER, x_vel = 14, y_vel = 0):
        super(Laser, self).__init__()
        self.sprite_sheet = setup.GFX['bulletss']
        
        self.name = name
        self.setup_frames()
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.state = c.START
        self.frame_index = 0
        self.animation_timer = 0
        self.image = self.frames[self.frame_index]
        self.hit = False
        self.rect = self.image.get_rect()
        self.rect.right = x
        self.rect.y = y
        self.damage = dmg
        if self.name == 'rocket':
            self.x_vel = 5


    def setup_frames(self):
        self.frames = []


        self.frames.append(
            self.get_image(0,0, 32, 32))
        self.frames.append(
            self.get_image(0,32, 32, 32))
        self.frames.append(
            self.get_image(0,64, 32, 32))
        self.frames.append(
            self.get_image(0,96, 32, 32))
        self.frames.append(
            self.get_image(0,128, 32, 32))

        if self.name == 'rocket':
            index = 0
        
            for image in self.frames:
                rect = image.get_rect()
                image = pg.transform.scale(image,
                                   (int(rect.width*0.3),
                                    int(rect.height*0.3)))
                self.frames[index] = image
                index += 1

    def get_image(self, x, y, width, height):
        """Get the image frames from the sprite sheet"""

        image = pg.Surface([width, height]).convert()
        rect = image.get_rect()

        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey((0,0,0))
        


        image = pg.transform.scale(image,
                                   (int(rect.width*1),
                                    int(rect.height*1)))
        return image

    def update(self, game_info):
        """Updates laser behavior"""
        self.current_time = game_info[c.CURRENT_TIME]
        self.handle_state()

    def handle_state(self):
        """Handles behavior based on state"""
        if self.state == c.START:
            self.animation()
            
        elif self.state == c.HIT:
            self.animation()

    def animation(self):
        if self.animation_timer == 0:
            self.animation_timer = self.current_time
        if self.state == c.START:
            if (self.current_time - self.animation_timer) > 40:
                if self.frame_index < 2:
                    self.frame_index += 1
                else:
                    self.frame_index = 2
                self.animation_timer = 0
                self.image = self.frames[self.frame_index]
        elif self.state == c.HIT:
            if (self.current_time - self.animation_timer)  > 60:
                if self.frame_index < 4:
                    self.frame_index += 1
                    self.image = self.frames[self.frame_index]
                    self.animation_timer = 0
                else:
                    self.kill()


    def hit_transition(self):
        #gör om laserns state till prick state om den prickar något
        self.frame_index = 2
        #centerx = self.rect.centerx
        self.image = self.frames[self.frame_index]
        #self.rect.centerx = centerx
        self.x_vel = 0
        self.y_vel = 0
        self.state = c.HIT
        

class Coin(Powerup):
    def __init__(self, x, y, value):
        super(Coin, self).__init__()
        self.value = value
        if self.value >= 100:
            self.sprite_sheet = setup.GFX['coin_gold']
        elif 10 >= self.value and self.value < 100:
            self.sprite_sheet = setup.GFX['silver_coin']
        elif 1 >= self.value and self.value < 10:
            self.sprite_sheet = setup.GFX['copper_coin']
        else:
            self.sprite_sheet = setup.GFX['silver_coin']
        self.setup_frames()
        self.x_vel = 0
        self.y_vel = 0
        self.state = c.START
        self.frame_index = 0
        self.animation_timer = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.right = x
        self.rect.y = y
        self.adds  = 1
        self.name = c.COIN

    def setup_frames(self):
        self.frames = []
        if self.value >= 100:
            self.frames.append(
                self.get_image(0,0,32,24))
            self.frames.append(
                self.get_image(32,0,32,24))
            self.frames.append(
                self.get_image(64,0,32,24))
            self.frames.append(
                self.get_image(96,0,32,24))
            self.frames.append(
                self.get_image(128,0,32,24))
            self.frames.append(
                self.get_image(160,0,32,24))
            self.frames.append(
                self.get_image(192,0,32,24))
            self.frames.append(
                self.get_image(224,0,32,24))
        else:
            self.frames.append(
                self.get_image(0,0,32,24))
            self.frames.append(
                self.get_image(0,32,32,24))
            self.frames.append(
                self.get_image(0,64,32,24))
            self.frames.append(
                self.get_image(0,96,32,24))
            self.frames.append(
                self.get_image(0,128,32,24))
            self.frames.append(
                self.get_image(0,160,32,24))
            self.frames.append(
                self.get_image(0,192,32,24))
            self.frames.append(
                self.get_image(0,0,32,24))

    def update(self, game_info):
        """Updates laser behavior"""
        self.current_time = game_info[c.CURRENT_TIME]
        self.handle_state()

    def handle_state(self):
        """Handles behavior based on state"""
        if self.state == c.START:
            self.animation()
            
        elif self.state == c.HIT:
            self.animation()

    def animation(self):
        if self.state == c.START:
            if (self.current_time - self.animation_timer) > 100:
                if self.frame_index < 7:
                    self.frame_index += 1
                else:
                    self.frame_index = 0
                self.animation_timer = self.current_time
                self.image = self.frames[self.frame_index]

    def get_image(self, x, y, width, height):
        """Get the image frames from the sprite sheet"""

        image = pg.Surface([width, height]).convert()
        rect = image.get_rect()

        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(c.BLACK)


        image = pg.transform.scale(image,
                                   (int(rect.width*0.5),
                                    int(rect.height*0.5)))
        return image

class Enemy_Laser(pg.sprite.Sprite):
    def __init__(self, x, y, dmg, name = None):
        super(Enemy_Laser, self).__init__()
        self.sprite_sheet = setup.GFX['RedLaser']
        self.setup_frames()
        self.x_vel = -3
        self.y_vel = 0
        self.state = c.START
        self.frame_index = 0
        self.animation_timer = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.right = x
        self.rect.y = y
        if name != None:
            self.name = name
        else:
            self.name = c.ENEMY_LASER
        if self.name == 'Viper_laser':
            self.x_vel = random.randint(-3,-1)
            self.y_vel = random.randint(-2,0)
            self.name = c.ENEMY_LASER
        self.dmg = dmg

    def setup_frames(self):
        self.frames = []

        self.frames.append(
            self.get_image(0, 0, 12, 12))

    def get_image(self, x, y, width, height):
        """Get the image frames from the sprite sheet"""

        image = pg.Surface([width, height]).convert()
        rect = image.get_rect()

        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        


        #image = pg.transform.scale(image,
        #                           (int(rect.width*c.SIZE_MULTIPLIER),
        #                            int(rect.height*c.SIZE_MULTIPLIER)))
        return image

    def update(self, game_info):
        """Updates laser behavior"""
        self.current_time = game_info[c.CURRENT_TIME]
        self.handle_state()

    def handle_state(self):
        """Handles behavior based on state"""
        if self.state == c.START:
            self.animation()
            
        elif self.state == c.HIT:
            self.animation()

    def animation(self):
        if self.state == c.START:
            if (self.current_time - self.animation_timer) > 200:
                if self.frame_index < 0:
                    self.frame_index += 1
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

    def hit_transition(self):
        #gör om laserns state till prick state om den prickar något
        self.frame_index = 1
        #centerx = self.rect.centerx
        self.image = self.frames[self.frame_index]
        #self.rect.centerx = centerx
        self.state = c.START