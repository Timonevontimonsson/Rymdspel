
import pygame as pg
from scripts.data import setup
from scripts.data import constant as c

class Digit(pg.sprite.Sprite):
    #individuella siffran för poängen
    def __init__(self, image):
        super(Digit, self).__init__()
        self.image = image
        self.rect = image.get_rect()

class Score(object):
    def __init__(self, x, y, score, color):
        self.x = x
        self.y  = y
        self.y_vel = -3
        self.color = color
        self.indicator = 0
        self.size = 1
        if self.color == 'white':
            self.size = 1
            self.indicator = 0
        elif self.color == 'green':
            self.indicator = 1
            self.size = 2
            self.y_vel = -1
        elif self.color == 'red':
            self.indicator = 2
            self.size = 2
            self.y_vel = -1
        self.sprite_sheet = setup.GFX['numbers_colors']
        self.create_image_dict()
        self.score_string = str(score)
        self.create_digit_list()
    def create_image_dict(self):
        """Creates the dictionary for all the number images needed"""
        self.image_dict = {}

        image0 = self.get_image(0, 0+8*self.indicator, 7, 7)
        image1 = self.get_image(9, 0+8*self.indicator, 7, 7)
        image2 = self.get_image(16, 0+8*self.indicator, 7, 7)
        image3 = self.get_image(24, 0+8*self.indicator, 7, 7)
        image4 = self.get_image(32, 0+8*self.indicator, 7, 7)
        image5 = self.get_image(40, 0+8*self.indicator, 7, 7)
        image6 = self.get_image(48, 0+8*self.indicator, 7, 7)
        image7 = self.get_image(56, 0+8*self.indicator, 7, 7)
        image8 = self.get_image(64, 0+8*self.indicator, 7, 7)
        image9 = self.get_image(7, 0+8*self.indicator, 7, 7)

        self.image_dict['0'] = image0
        self.image_dict['1'] = image1
        self.image_dict['2'] = image2
        self.image_dict['3'] = image3
        self.image_dict['4'] = image4
        self.image_dict['5'] = image5
        self.image_dict['6'] = image6
        self.image_dict['7'] = image7
        self.image_dict['8'] = image8
        self.image_dict['9'] = image9

    def get_image(self, x, y, width, height):
        """Extracts image from sprite sheet"""
        image = pg.Surface([width, height]).convert()
        rect = image.get_rect()

        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
      
        
        #transColor = image.get_at((0,0))
        #image.set_colorkey(transColor)
        image.set_colorkey((0,0,0))

        image = pg.transform.scale(image,
                                   (int(rect.width*self.size),
                                    int(rect.height*self.size)))
        return image

    def create_digit_list(self):
        """Creates the group of images based on score received"""
        self.digit_list = []
        self.digit_group = pg.sprite.Group()
       

        for digit in self.score_string:
            self.digit_list.append(Digit(self.image_dict[digit]))

        self.set_rects_for_images()


    def set_rects_for_images(self):
        """Set the rect attributes for each image in self.image_list"""
        for i, digit in enumerate(self.digit_list):
            digit.rect = digit.image.get_rect()
            if self.color == 'white':
                digit.rect.x = self.x + (i * 10)
            elif self.color == 'red' or self.color == 'green':
                digit.rect.x = self.x + (i * 14)
            digit.rect.y = self.y


    def update(self, score_list, level_info):
        """Updates score movement"""
        for number in self.digit_list:
            number.rect.y += self.y_vel

        if score_list:
            self.check_to_delete_floating_scores(score_list, level_info)
            



    def draw(self, screen):
        """Draws score numbers onto screen"""
        for digit in self.digit_list:
            screen.blit(digit.image, digit.rect)

    def check_to_delete_floating_scores(self, score_list, level_info):
        """Check if scores need to be deleted"""
        for i, score in enumerate(score_list):
            if self.color == 'white':
                if (score.y - score.digit_list[0].rect.y) > 100:
                    score_list.pop(i)

            else:
                if (score.y - score.digit_list[0].rect.y) > 110:
                    score_list.pop(i)