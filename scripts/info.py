
import pygame as pg
from scripts.data import setup
from scripts.data import constant as c
from scripts.data import animated_coin

class Character(pg.sprite.Sprite):
    def __init__(self, image):
        super(Character, self).__init__()
        self.image = image
        self.rect = self.image.get_rect()


class OverheadInfo(object):
    'class for level information like score, money and hp'

    def __init__(self, game_info, state):
        self.sprite_sheet = setup.GFX['text_images']
        self.goal_sheet = setup.GFX['goal_ui']
        self.healthbar_sheet = setup.GFX['healthbar']
        self.ui_img = setup.GFX['UI']
        
        self.health = game_info[c.HEALTH]
        self.top_score = game_info[c.TOP_SCORE]
        self.current_time = 0
        self.state = state
        self.special_state = None
        self.game_info = game_info
        self.goal_frame_index = 0
        self.healthbar_frame_index = 0

        self.ui = self.get_image_ui(0,0,1100,100)
        self.moving_coin = animated_coin.Animated_coin(300,40)

        self.create_image_dict()
        self.create_score_group()
        self.create_info_labels()
        self.create_goal_indicator()
        self.create_healthbar()

        #self.create_load_screen_labels()
        #self.create_countdown_clock()
        #self.create_coin_counter()
        #self.create_flashing_coin()
        #self.create_mario_image()
        #self.create_game_over_label()
        #self.create_time_out_label()
        #self.create_main_menu_labels()

    def create_image_dict(self):
        """Creates the initial images for the score"""
        self.image_dict = {}
        image_list = []

        image_list.append(self.get_image(3, 230, 7, 7))
        image_list.append(self.get_image(12, 230, 7, 7))
        image_list.append(self.get_image(19, 230, 7, 7))
        image_list.append(self.get_image(27, 230, 7, 7))
        image_list.append(self.get_image(35, 230, 7, 7))
        image_list.append(self.get_image(43, 230, 7, 7))
        image_list.append(self.get_image(51, 230, 7, 7))
        image_list.append(self.get_image(59, 230, 7, 7))
        image_list.append(self.get_image(67, 230, 7, 7))
        image_list.append(self.get_image(75, 230, 7, 7))

        image_list.append(self.get_image(83, 230, 7, 7))
        image_list.append(self.get_image(91, 230, 7, 7))
        image_list.append(self.get_image(99, 230, 7, 7))
        image_list.append(self.get_image(107, 230, 7, 7))
        image_list.append(self.get_image(115, 230, 7, 7))
        image_list.append(self.get_image(123, 230, 7, 7))
        image_list.append(self.get_image(3, 238, 7, 7))
        image_list.append(self.get_image(11, 238, 7, 7))
        image_list.append(self.get_image(20, 238, 7, 7))
        image_list.append(self.get_image(27, 238, 7, 7))
        image_list.append(self.get_image(35, 238, 7, 7))
        image_list.append(self.get_image(44, 238, 7, 7))
        image_list.append(self.get_image(51, 238, 7, 7))
        image_list.append(self.get_image(59, 238, 7, 7))
        image_list.append(self.get_image(67, 238, 7, 7))
        image_list.append(self.get_image(75, 238, 7, 7))
        image_list.append(self.get_image(83, 238, 7, 7))
        image_list.append(self.get_image(91, 238, 7, 7))
        image_list.append(self.get_image(99, 238, 7, 7))
        image_list.append(self.get_image(108, 238, 7, 7))
        image_list.append(self.get_image(115, 238, 7, 7))
        image_list.append(self.get_image(123, 238, 7, 7))
        image_list.append(self.get_image(3, 246, 7, 7))
        image_list.append(self.get_image(11, 246, 7, 7))
        image_list.append(self.get_image(20, 246, 7, 7))
        image_list.append(self.get_image(27, 246, 7, 7))
        image_list.append(self.get_image(48, 248, 7, 7))

        image_list.append(self.get_image(68, 249, 6, 2))
        image_list.append(self.get_image(75, 247, 6, 6))



        character_string = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ -*'

        for character, image in zip(character_string, image_list):
            self.image_dict[character] = image


    def get_image(self, x, y, width, height):
        """Extracts image from sprite sheet"""
        image = pg.Surface([width, height])
        rect = image.get_rect()

        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey((92, 148, 252))
        image = pg.transform.scale(image,
                                   (int(rect.width*2),
                                    int(rect.height*2)))
        return image
    def get_image_goal(self, x, y, width, height):
        """Extracts image from sprite sheet"""
        image = pg.Surface([width, height])
        rect = image.get_rect()

        image.blit(self.goal_sheet, (0, 0), (x, y, width, height))
        
        image = pg.transform.scale(image,
                                   (int(rect.width*1),
                                    int(rect.height*1)))
        return image

    def get_image_healthbar(self, x, y, width, height):
        """Extracts image from sprite sheet"""
        image = pg.Surface([width, height])
        rect = image.get_rect()

        image.blit(self.healthbar_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey((0,0,0))
        
        image = pg.transform.scale(image,
                                   (int(rect.width*2),
                                    int(rect.height*1.5)))
        return image
    def get_image_ui(self, x, y, width, height):
        """Extracts image from sprite sheet"""
        image = pg.Surface([width, height])
        rect = image.get_rect()

        image.blit(self.ui_img, (0, 0), (x, y, width, height))
        image.set_colorkey((0,0,0))
        
        image = pg.transform.scale(image,
                                   (int(rect.width*1),
                                    int(rect.height*1)))
        return image
    def update_healthbarr(self, width):
        image = pg.Surface([width, 45])
        rect = image.get_rect()

        image.blit(self.healthbar_sheet, (0,0), (0, 27, width, 45))
        image = pg.transform.scale(image,
                                   (int(rect.width*2),
                                    int(rect.height*1.5)))
        image.set_colorkey((0,0,0))
        return image
    def create_label(self, label_list, string, x, y):
        """Det här skapar en text"""
        for letter in string:
            label_list.append(Character(self.image_dict[letter]))

        self.set_label_rects(label_list, x, y)

    def set_label_rects(self, label_list, x, y):
        """Set the location of each individual character"""
        for i, letter in enumerate(label_list):
            letter.rect.x = x + ((letter.rect.width + 3) * i)
            letter.rect.y = y
            if letter.image == self.image_dict['-']:
                letter.rect.y += 7
                letter.rect.x += 2
    def create_goal_indicator(self):
        self.goal_frames = []

        for i in range(12):
             self.goal_frames.append(
                 self.get_image_goal(0,0+i*30,200,30))

    def create_healthbar(self):
        self.healthbar_frames = []

        
        self.healthbar_frames.append(
                self.get_image_healthbar(0, 27, 85, 45))
        self.healthbar_frames.append(
                self.get_image_healthbar(0, 27+1000, 85, 45))

    def create_score_group(self):
        'Det här skapar start texten med tomt score (000000000)'
        self.score_images = []
        self.create_label(self.score_images, '             ', 200, 46)
        #UPDATES

    def create_info_labels(self):
        self.score_label = []
        self.new_game_label = []
        self.quit_label = []
        

        self.create_label(self.score_label, 'SCORE', 170, 10)
        self.create_label(self.new_game_label, 'NEW GAME', 400, 240)
        self.create_label(self.quit_label, 'QUIT', 400, 405)
        

        self.main_menu_labels = [
                           self.new_game_label,
                           self.quit_label]

        #self.game_labels = [self.score_label]


    def update_score_images(self, images, score):
        #Uppdaterar vilka nummer som ska vara på skärmen
        index = 0
        self.money = setup.myfont_money.render(str(self.player.inventory['gold']), 1, (c.YELLOW))
        for digit in str(self.player.inventory['gold']):
            rect = images[index].rect
            images[index] = Character(self.image_dict[digit])
            images[index].rect = rect
            index += 1

    def update_goal_image(self, score):
        if self.goal_frame_index < 11:
            self.goal_frame_index = int(score/100_000)
        else:
            self.goal_frame_index = 11

    def update_healthbar(self):
        limit = self.player.max_health/82
        
        if self.player.health >= 0:
             self.healthbar_frames[0] = self.update_healthbarr(int(self.player.health/limit))

        self.moving_coin.update(self.current_time)
        

    def update(self, level_info, player=None,current_time=None):
        """Updates all overhead info"""
        self.current_time = current_time
        self.player = player
        self.handle_level_state(level_info)

    def handle_level_state(self, level_info):
        """Updates info based on what state the game is in"""
        if self.state == c.MAIN_MENU:
            self.score = level_info[c.SCORE]
            #self.update_score_images(self.score_images, self.score)
            #self.update_score_images(self.main_menu_labels[3], self.top_score)
            #self.update_coin_total(level_info)
            #self.flashing_coin.update(level_info[c.CURRENT_TIME])

        elif self.state == c.LOAD_SCREEN:
            self.score = level_info[c.SCORE]
            #self.update_score_images(self.score_images, self.score)
            #self.update_coin_total(level_info)

        elif self.state == c.LEVEL:
            self.score = level_info[c.SCORE]
            self.update_score_images(self.score_images, self.score)
            #self.update_goal_image(self.score)
            self.update_healthbar()

            #self.update_coin_total(level_info)
            #self.flashing_coin.update(level_info[c.CURRENT_TIME])

        elif self.state == c.TIME_OUT:
            self.score = level_info[c.SCORE]
            self.update_score_images(self.score_images, self.score)
            self.update_coin_total(level_info)

        elif self.state == c.GAME_OVER:
            self.score = level_info[c.SCORE]
            self.update_score_images(self.score_images, self.score)
            self.update_coin_total(level_info)

        elif self.state == c.FAST_COUNT_DOWN:
            level_info[c.SCORE] += 50
            self.score = level_info[c.SCORE]
            self.update_count_down_clock(level_info)
            self.update_score_images(self.score_images, self.score)
            self.update_coin_total(level_info)
            self.flashing_coin.update(level_info[c.CURRENT_TIME])
            if self.time == 0:
                self.state = c.END_OF_LEVEL

        elif self.state == c.END_OF_LEVEL:
            self.flashing_coin.update(level_info[c.CURRENT_TIME])

    def draw(self, surface):
        """Draws overhead info based on state"""
        if self.state == c.MAIN_MENU:
            self.draw_main_menu_info(surface)
        elif self.state == c.LOAD_SCREEN:
            self.draw_loading_screen_info(surface)
        elif self.state == c.LEVEL:
            self.draw_level_screen_info(surface)
        elif self.state == c.GAME_OVER:
            self.draw_game_over_screen_info(surface)
        elif self.state == c.VICTORY:
            self.draw_level_screen_info(surface)
        else:
            pass

    def draw_main_menu_info(self, surface):
        """Draws info for main menu"""
        

        #for info in self.score_images:
           # surface.blit(info.image, info.rect)

        for label in self.main_menu_labels:
            for letter in label:
                surface.blit(letter.image, letter.rect)

        #for character in self.coin_count_images:
        #    surface.blit(character.image, character.rect)

        #for label in self.label_list:
         #   for letter in label:
          #      surface.blit(letter.image, letter.rect)

        #surface.blit(self.flashing_coin.image, self.flashing_coin.rect)

    def draw_loading_screen_info(self, surface):
        #ritar info för loadingscreen

        surface.blit(self.ui, (0,0))

        for info in self.score_images:
            surface.blit(info.image, info.rect)


        #for word in self.center_labels:
        #    for letter in word:
        #        surface.blit(letter.image, letter.rect)

        #for word in self.life_total_label:
        #    surface.blit(word.image, word.rect)

        #surface.blit(self.mario_image, self.mario_rect)
        #surface.blit(self.life_times_image, self.life_times_rect)

        #for character in self.coin_count_images:
        #    surface.blit(character.image, character.rect)

        #for label in self.label_list:
         #   for letter in label:
          #      surface.blit(letter.image, letter.rect)

        #surface.blit(self.flashing_coin.image, self.flashing_coin.rect)

    def draw_level_screen_info(self, surface):
        surface.blit(self.ui, (0,0))

       # for info in self.score_images:
          #  surface.blit(info.image, info.rect)
        #for label in self.game_labels:
           # for letter in label:
              #  surface.blit(letter.image, letter.rect)
        surface.blit(self.money, (200,40))
        
        #surface.blit(self.goal_frames[self.goal_frame_index], (20, c.SCREEN_HEIGHT - 50))
        surface.blit(self.healthbar_frames[1], (-1, 45))
        surface.blit(self.healthbar_frames[0], (-1, 45))
        surface.blit(self.moving_coin.image, (166, self.moving_coin.rect.y))