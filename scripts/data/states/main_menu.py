
import pygame as pg
from scripts.data import tools, setup
from scripts.data import constant as c
from scripts import info, player
from scripts.data.states import level1

keybinding = {
        'left':pg.K_a,
        'right':pg.K_d,
        'up':pg.K_w,
        'down':pg.K_s,
        'skill':pg.K_SPACE,
        'dash':pg.K_LSHIFT
    }
class Menu(tools._State):
    def __init__(self):
        """initializes the state"""
        tools._State.__init__(self)
        persist = {c.SCORE: 0,
                   c.TOP_SCORE: 0,
                   c.HEALTH: 3,
                   c.CURRENT_TIME: 0.0,
                   c.LEVEL_STATE: None,
                   c.PLAYER_DEAD: False,
                   c.LEVEL: None
                   }

        self.player = player.Player()
        self.startup(0.0,persist, self.player)

        tools.keyPressed = []
        tools.keyReleased = []

        self.X1 = 0
        self.X2 = c.SCREEN_WIDTH


    def startup(self,current_time, persist, player):
        """Called every time the game's state becomes this one.  Initializes
        certain values"""
        self.next = c.LEVEL1
        self.persist = persist
        self.game_info = persist
        self.player
        self.overhead_info = info.OverheadInfo(self.game_info, c.MAIN_MENU)
        

        self.sprite_sheet = setup.GFX['title_screen']
        self.setup_background()
        self.setup_player()
        self.setup_cursor()

    def setup_cursor(self):
        """Skapar cursorn"""
        self.cursor = pg.sprite.Sprite()
        dest = (360, 240)
        self.cursor.image, self.cursor.rect = self.get_image(5, 111, 24, 22, dest, setup.GFX['title_screen'])
        self.cursor.state = c.PLAYER1

    def setup_player(self):
        
        self.player = player.Player()
        self.player.rect.x = 110
        self.player.rect.bottom = 200
        

    def setup_background(self):
        self.background = setup.GFX['background']

        self.image_dict = {}
        self.image_dict['GAME_NAME_BOX'] = self.get_image(
            5, 5, 472, 96, (314, 50), setup.GFX['title_screen'])


    def get_image(self, x, y, width, height, dest, sprite_sheet):
        """Returns images and rects to blit onto the screen"""
        image = pg.Surface([width, height])
        rect = image.get_rect()

        image.blit(sprite_sheet, (0, 0), (x, y, width, height))
        if sprite_sheet == setup.GFX['title_screen']:
            image.set_colorkey((255, 0, 220))
            image = pg.transform.scale(image,
                                   (int(rect.width*c.SIZE_MULTIPLIER),
                                    int(rect.height*c.SIZE_MULTIPLIER)))
        else:
            image.set_colorkey(c.BLACK)
            image = pg.transform.scale(image,
                                   (int(rect.width*3),
                                    int(rect.height*3)))

        rect = image.get_rect()
        rect.x = dest[0]
        rect.y = dest[1]
        return (image, rect)

    def update(self, surface, keys, current_time):
     #Uppdaterar state varje refresh
         #self.update_cursor(keys)
         
         self.update_cursor(keys)
         self.update_background()
         self.current_time = current_time
         self.overhead_info.update(self.game_info)
         self.game_info[c.CURRENT_TIME] = self.current_time
         #lägg till scrollande bakgrund här
         surface.blit(self.background, (self.X1, 0))
         surface.blit(self.background, (self.X2, 0))
         surface.blit(self.image_dict['GAME_NAME_BOX'][0],
                      self.image_dict['GAME_NAME_BOX'][1])
         surface.blit(self.player.image, self.player.rect)
         surface.blit(self.cursor.image, self.cursor.rect)
         self.overhead_info.draw(surface)

    def update_background(self):
        self.X1 -= 1.4
        self.X2 -= 1.4

        if self.X1 < -1100:
            self.X1 = c.SCREEN_WIDTH
        if self.X2  < -1100:
            self.X2 = c.SCREEN_WIDTH


    def update_cursor(self, keys):
        input_list = [pg.K_RETURN]
        
        if self.cursor.state == c.PLAYER1:
            self.cursor.rect.y = 240
            if tools.keybinding['down'] in tools.keyPressed:
                self.cursor.state = c.SHOP
                tools.keyPressed.remove(tools.keybinding['down'])
            for input in input_list:
                if tools.keybinding['enter'] in tools.keyPressed:
                    self.persist[c.LEVEL] = c.LEVEL_1
                    self.next = c.LEVEL1
                    self.done = True
                    tools.keyPressed.remove(tools.keybinding['enter'])
        elif self.cursor.state == c.SHOP:
            self.cursor.rect.y = 300
            if tools.keybinding['up'] in tools.keyPressed:
                self.cursor.state = c.PLAYER1
                tools.keyPressed.remove(tools.keybinding['up'])
            elif tools.keybinding['down'] in tools.keyPressed:
                self.cursor.state = c.QUIT
                tools.keyPressed.remove(tools.keybinding['down'])
        elif self.cursor.state == c.QUIT:
            self.cursor.rect.y = 403
            if tools.keybinding['up'] in tools.keyPressed:
                self.cursor.state = c.SHOP
                tools.keyPressed.remove(tools.keybinding['up'])

    def reset_game_info(self):
        self.game_info[c.SCORE] = 0
        self.game_info[c.LEVEL_STATE] = None

        self.persist = self.game_info

