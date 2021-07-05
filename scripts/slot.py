import pygame as pg
from scripts.data import setup, tools
from scripts.data import constant as c




class Slot(pg.sprite.Sprite):
    def __init__(self, id, x, y):
        pg.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.id = id
        self.empty_slot = setup.GFX['slot']
        self.highlight_slot = setup.GFX['slot_highlighted']
        self.clicked_slot = setup.GFX['slot_clicked']
        self.green_slot = setup.GFX['green-slot']
        self.blue_slot = setup.GFX['blue-slot']
        self.orange_slot = setup.GFX['orange-slot']
        self.red_slot = setup.GFX['red-slot']
        self.coin_image = setup.GFX['Coin']
        self.coin_image = pg.transform.scale(self.coin_image, (9,9))
        

        self.number_font = setup.myfont
        self.item_title_font = setup.myfont_itemtitle
        self.state = c.SLOT_DEFAULT

        self.image = self.empty_slot
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.top = y
        self.tempx = x
        self.tempy = y
        self.highlight_slot.set_colorkey((0,0,0))
        self.clicked_slot.set_colorkey((0,0,0))
        self.green_slot.set_colorkey((0,0,0))
        
        

        self.item = None
        self.item_rect = self.image.get_rect()
        self.item_rect.x = self.rect.x
        self.item_rect.top = self.rect.top
        self.item_carry = False
        self.item_quantity = 0
        self.item_picture = None
        self.item_grey_picture = None
        self.rescale_toggle = False
        #self.icon = image av grejen

    def update(self, event = 1):
        if event == 1:
            if self.state != c.SLOT_DEFAULT:
                self.state = c.SLOT_DEFAULT
                self.handle_states()
        elif event == 2:
            self.state = c.SLOT_HIGHLIGHTED
            self.handle_states()
        elif event == 3:
            self.state = c.SLOT_CLICKED
            self.handle_states()
        
    def handle_states(self):
        None
        #if self.state == c.SLOT_DEFAULT:
        #    self.image = self.empty_slot
        #elif self.state == c.SLOT_HIGHLIGHTED:
        #    self.image = self.highlight_slot
        #elif self.state == c.SLOT_CLICKED:
        #    self.image = self.clicked_slot

    def set_item(self, item):
        self.item = item

    def reset(self):
        self.item_rect.x = self.rect.x
        self.item_rect.top = self.rect.top

        self.item = None
        self.item_rect = self.image.get_rect()
        self.item_rect.x = self.rect.x
        self.item_rect.top = self.rect.top
        self.item_carry = False
        self.item_quantity = 0
        self.item_picture = None
        self.item_grey_picture = None
        self.rescale_toggle = False


    def grayscale(self, img):
        arr = pg.surfarray.array3d(img)
        #luminosity filter
        avgs = [[(r*0.298 + g*0.587 + b*0.114) for (r,g,b) in col] for col in arr]
        arr=arr.dot([0.298, 0.587, 0.114])[:,:,None].repeat(3,axis=2); 
        return pg.surfarray.make_surface(arr)
        
    #def add_item(self, item, quantity):
    #    if self.item != None:
    #        if self.item.id == item:
    #            self.item_quantity += quantity
    #    else:
    #        self.item = setup.items[item]

    #        self.item_picture = setup.items_pictures[item]
    #        self.item_picture = pg.transform.scale(self.item_picture, (42,42))
    #        self.item_grey_picture = self.grayscale(self.item_picture)
    #        self.item_quantity = quantity

    def add_item(self, item, quantity, type):
            if type == 'misc':
                    
                    if self.item != None:
                        if self.item.id == item:
                            self.item_quantity += quantity
                    else:
                        self.item = setup.items[item]

                        self.item_picture = setup.items_pictures[item]
                        self.item_picture = pg.transform.scale(self.item_picture, (42,42))
                        self.item_grey_picture = self.grayscale(self.item_picture)
                        self.item_quantity = quantity
            elif type == 'Weapon':
                self.item = setup.weapons[item]
                self.item_picture = setup.weapons_pictures[item]
                self.item_grey_picture = self.grayscale(self.item_picture)
                self.item_quantity = 0
                self.rescale_item()
            elif type == 'Armor':
                self.item = setup.armors[item]
                self.item_picture = setup.armors_pictures[item]
                self.item_grey_picture = self.grayscale(self.item_picture)
                self.item_quantity = 0
                self.rescale_item()
            
            #self.rescale_item()


    def rescale_item(self):
       # if self.rescale_toggle == False:
            self.item_picture = pg.transform.scale(self.item_picture, (40,39))
            self.item_grey_picture = pg.transform.scale(self.item_grey_picture, (40,39))
            self.green_slot = pg.transform.scale(self.green_slot, (45,45))
            self.blue_slot = pg.transform.scale(self.blue_slot, (45,45))
            self.orange_slot = pg.transform.scale(self.orange_slot, (45,45))
            self.red_slot = pg.transform.scale(self.red_slot, (45,45))

            self.rescale_toggle = True

            

    def blit_alpha(self, target, source, location, opacity):
        x = location[0]
        y = location[1]
        temp = pg.Surface((source.get_width(), source.get_height())).convert()
        temp.blit(target, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)        
        target.blit(temp, location)

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.top))
        if self.state == c.SLOT_HIGHLIGHTED:
            self.blit_alpha(surface, self.highlight_slot, (self.rect.x, self.rect.top), 50)
        if self.item_carry == False:
            if self.state == c.SLOT_CLICKED:
                self.blit_alpha(surface, self.clicked_slot, (self.rect.x, self.rect.top), 50)
    def draw_tooltip(self, surface):
        if self.item.rarity == 'White':
            self.item_title_lbl = self.item_title_font.render(self.item.name, 1, (c.WHITE))
        elif self.item.rarity == 'Green':
            self.item_title_lbl = self.item_title_font.render(self.item.name, 1, (c.FOREST_GREEN))
        elif self.item.rarity == 'Blue':
            self.item_title_lbl = self.item_title_font.render(self.item.name, 1, (c.BLUE))
        if self.item.rarity == 'Orange':
            self.item_title_lbl = self.item_title_font.render(self.item.name, 1, (c.ORANGE))
        if self.item.rarity == 'Red':
            self.item_title_lbl = self.item_title_font.render(self.item.name, 1, (c.RED))
        self.item_rarity_lbl = self.number_font.render(self.item.type, 1, (255,255,255))
        self.item_cost_lbl = self.number_font.render('Sell price: ' + str(self.item.value), 1, (c.WHITE))
        text_width = self.calculate_rect_width()
        if self.item.type == 'misc' or self.item.type == 'Armor':
            text_height = 37
        elif self.item.type == 'Weapon':
            text_height = 48
            self.item_dmg_lbl = self.number_font.render('Damage: ' + str(self.item.damage), 1, (c.FOREST_GREEN))
        pg.draw.rect(surface, (c.BLACK), (self.rect.x+46, self.rect.top-text_height-3, text_width+3, text_height+3))
        pg.draw.line(surface, (192,192,192), (self.rect.x+46, self.rect.top-text_height-3), (self.rect.x+50+text_width, self.rect.top-text_height-3))
        pg.draw.line(surface, (192,192,192), (self.rect.x+46, self.rect.top-2), (self.rect.x+50+text_width, self.rect.top-2))
        pg.draw.line(surface, (192,192,192), (self.rect.x+46, self.rect.top-2), (self.rect.x+46, self.rect.top-text_height-3))
        pg.draw.line(surface, (192,192,192), (self.rect.x+50+text_width, self.rect.top-2), (self.rect.x+50+text_width, self.rect.top-text_height-3))
        surface.blit(self.item_title_lbl, (self.rect.x+48, self.rect.top-text_height-4))
        surface.blit(self.item_rarity_lbl, (self.rect.x+48, self.rect.top-text_height+10))
        if self.item.type == 'Weapon':
            surface.blit(self.item_dmg_lbl, (self.rect.x+48, self.rect.top-text_height+21))
        surface.blit(self.coin_image, (self.rect.x+48, self.rect.top-13))
        surface.blit(self.item_cost_lbl, (self.rect.x+59, self.rect.top-16))

    def calculate_rect_width(self):
        text_width = self.item_title_lbl.get_width()
        if self.item_rarity_lbl.get_width() > text_width:
            return self.item_rarity_lbl.get_width()
        else:
            return text_width

    #Här har vi allt som måste med
    def update_highlight(self):
        if self.rect.collidepoint(pg.mouse.get_pos()):
            self.update(2)
        elif self.state != c.SLOT_DEFAULT and "mouse" not in tools.keyPressed:
            self.update()


    def draw_item(self, surface):
        self.quantity_lbl = self.number_font.render(str(self.item_quantity), 1, (255,255,255))
        

        if self.item_carry == True:
            surface.blit(self.empty_slot, (self.rect.x, self.rect.top))
            surface.blit(self.item_grey_picture, (self.rect.x+3, self.rect.top+3))
            surface.blit(self.quantity_lbl, (self.rect.x+33, self.rect.top+33))
            if self.item.rarity == 'Green':
                self.blit_alpha(surface, self.green_slot, (self.rect.x, self.rect.top), 50)
            elif self.item.rarity == 'Blue':
                self.blit_alpha(surface, self.blue_slot, (self.rect.x, self.rect.top), 50)
            elif self.item.rarity == 'Orange':
                self.blit_alpha(surface, self.orange_slot, (self.rect.x, self.rect.top), 50)
            elif self.item.rarity == 'Red':
                self.blit_alpha(surface, self.red_slot, (self.rect.x, self.rect.top), 50)
            surface.blit(self.item_picture, (self.item_rect.x, self.item_rect.top))

        if self.item_carry == False:
            surface.blit(self.empty_slot, (self.rect.x, self.rect.top))
            surface.blit(self.item_picture, (self.item_rect.x+3, self.item_rect.top+3))
            if self.item.rarity == 'Green':
                self.blit_alpha(surface, self.green_slot, (self.rect.x, self.rect.top), 100)
            elif self.item.rarity == 'Blue':
                self.blit_alpha(surface, self.blue_slot, (self.rect.x, self.rect.top), 100)
            elif self.item.rarity == 'Orange':
                self.blit_alpha(surface, self.orange_slot, (self.rect.x, self.rect.top), 100)
            elif self.item.rarity == 'Red':
                self.blit_alpha(surface, self.red_slot, (self.rect.x, self.rect.top), 100)
            if self.state == c.SLOT_HIGHLIGHTED:
                self.draw_tooltip(surface)
                self.blit_alpha(surface, self.highlight_slot, (self.rect.x, self.rect.top), 50)
            elif self.state == c.SLOT_CLICKED:
                self.blit_alpha(surface, self.clicked_slot, (self.rect.x, self.rect.top), 50)
            if self.item_quantity != 0:
                if self.item_quantity < 100:
                    surface.blit(self.quantity_lbl, (self.rect.x+33, self.rect.top+33))
                elif self.item_quantity >= 100:
                    surface.blit(self.quantity_lbl, (self.rect.x+25, self.rect.top+33))

class EquipSlot(Slot):
    def __init__(self, id, x, y, type):
        Slot.__init__(self, id, x, y)
        self.empty_slot = pg.transform.scale(self.empty_slot, (24,24))
        self.highlight_slot = pg.transform.scale(self.highlight_slot, (24,24))
        self.image = self.empty_slot
        self.image = self.empty_slot
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.top = y
        self.type = type
        self.rescale_toggle = False

    def add_item(self, item, quantity, type):
        if self.type == type:
            if self.type == 'Weapon':
                self.item = setup.weapons[item]
                self.item_picture = setup.weapons_pictures[item]
                self.item_grey_picture = self.grayscale(self.item_picture)
            elif self.type == 'Armor':
                self.item = setup.armors[item]
                self.item_picture = setup.armors_pictures[item]
                self.item_grey_picture = self.grayscale(self.item_picture)
            self.rescale_item()
    def rescale_item(self):
        if self.rescale_toggle == False:
            self.item_picture = pg.transform.scale(self.item_picture, (20,19))
            self.green_slot = pg.transform.scale(self.green_slot, (24,24))
            self.blue_slot = pg.transform.scale(self.blue_slot, (24,24))
            self.orange_slot = pg.transform.scale(self.orange_slot, (24,24))
            self.red_slot = pg.transform.scale(self.red_slot, (24,24))
            self.rescale_toggle = True
       
class ShopSlot(Slot):
    def __init__(self, id, x, y):
        Slot.__init__(self, id, x, y)
        self.item_quantity = 0

    def draw_tooltip(self, surface):
        None

    def draw_info(self, surface):
        self.cost_lbl = self.number_font.render(str(self.item.value*4), 1, (255,255,255))

        surface.blit(self.coin_image, (self.rect.x+50, self.rect.top+33))
        surface.blit(self.cost_lbl, (self.rect.x+61, self.rect.top+30))