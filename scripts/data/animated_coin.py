import pygame as pg
from scripts.data import setup
from scripts.data import constant as c


class Animated_coin():
    def __init__(self, x, y):
        super(Animated_coin, self).__init__()
        self.sprite_sheet = setup.GFX['coin_gold']
        self.setup_frames()
        self.frame_index = 0
        self.animation_timer = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.right = x
        self.rect.y = y

    def setup_frames(self):
        self.frames = []

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

    def update(self, current_time):
        """Updates laser behavior"""
        self.current_time = current_time
        self.handle_state()

    def handle_state(self):
        """Handles behavior based on state"""
        self.animation()
    def animation(self):
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
        image.set_colorkey((0,0,0))


        image = pg.transform.scale(image,
                                   (int(rect.width*1.2),
                                    int(rect.height*1.2)))
        return image