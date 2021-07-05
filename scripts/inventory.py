from scripts.data import setup
from scripts.data import constant as c
from scripts import slot
import pygame as pg
from scripts import button


class Inventory(pg.sprite.Sprite):
    def __init__(self, size):
        pg.sprite.Sprite.__init__(self)
        self.x = 10
        self.y = 370
        self.inventory_slots = pg.sprite.Group()
        self.image = setup.GFX['backpack']
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.top = self.y
        self.size = size
        
       
        for i in range(size):
            y = int(i/8)
            x = ((i/8)-y)*8
            self.inventory_slots.add(slot.Slot(i+1, self.x+50*x, 50+self.y+50*y))


    def add_item_to_slot(self, item, quantity,type):
        toggle = False
        for slots in self.inventory_slots:
            if slots.item != None:
                if slots.item.id == item and slots.item_quantity+quantity < slots.item.stack or slots.item.stack == 0 and slots.item.type == type:
                    slots.add_item(item, quantity, type)
                    toggle = True
                    break
                elif slots.item_quantity != slots.item.stack and slots.item.id == item:
                    quantity -= slots.item.stack-slots.item_quantity
                    slots.add_item(item, int(slots.item.stack-slots.item_quantity))
                    for slot in self.inventory_slots:
                        if slot.item == None and quantity != 0:
                            slot.add_item(item, int(quantity))
                            slot.item_rect.x = slot.rect.x
                            slot.item_rect.top = slot.rect.top
                            toggle = True
                            quantity = 0
                            break
        if toggle == False:
            for slots in self.inventory_slots:
                if slots.item == None and quantity > 0:
                    slots.add_item(item, quantity, type)
                    slots.item_rect.x = slots.rect.x
                    slots.item_rect.top = slots.rect.top
                    break
    def draw(self, surface):
        #surface.blit(self.image, (self.rect.x, self.rect.top))
       
        for slot in self.inventory_slots:
            if slot.item == None or slot.item_carry == True:
                slot.draw(surface)
        for slot in self.inventory_slots:
            if slot.item != None and slot.item_carry == False:
                slot.draw_item(surface)
        for slot in self.inventory_slots:
            if slot.item_carry == True:
                slot.draw_item(surface)
        

    def check_state(self):
        svar = "nej"
        for slot in self.inventory_slots:
            if slot.state == c.SLOT_CLICKED:
                svar = "ja"
            else:
                None
        if svar == "nej":
            return True
        else:
            return False

class Equipment(pg.sprite.Sprite):
    def __init__(self, ship):
            pg.sprite.Sprite.__init__(self)
            self.x = 500
            self.y = 200
            self.equipment_slots = pg.sprite.Group()
            self.image = setup.GFX['equipment-tab']
            self.button_group = []

            self.button_group.append(button.Button(rect=(750,120,50,20), command = self.btn_weapon_pressed, picture = 'btn-left'))
            self.button_group.append(button.Button(rect=(985,120,50,20), command = self.btn_armor_pressed, picture = 'btn-right'))


            
            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.top = self.y
            self.ship = ship
            self.state_type = 'Weapon'
            if self.ship == 'phoenix':
                self.ship_image = setup.GFX['spaceshipcool']
                self.ship_image = self.get_image(0,0,72,48)
                self.size_weapon = 4
                self.size_armor = 2
            for i in range(self.size_weapon):
                y = int(i/9)
                x = ((i/9)-y)*9
                self.equipment_slots.add(slot.EquipSlot(i+1, self.x+25*x+245, 25+self.y+25*y+44, 'Weapon'))
            for i in range(self.size_armor):
                y = int(i/9)
                x = ((i/9)-y)*9
                self.equipment_slots.add(slot.EquipSlot(i+1+self.size_weapon, self.x+25*x+245, 25+self.y+25*y+44, 'Armor'))
    def get_image(self, x, y, width, height):
        """Extracts image from sprite sheet"""
        image = pg.Surface([width, height])
        rect = image.get_rect()

        image.blit(self.ship_image, (0, 0), (x, y, width, height))
        image.set_colorkey(c.BLACK)
        image = pg.transform.scale(image,
                                   (int(rect.width*1.5),
                                    int(rect.height*1.5)))
        return image
    def btn_weapon_pressed(self):
        self.state_type = 'Weapon'

    def btn_armor_pressed(self):
        self.state_type = 'Armor'


    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.top))
        surface.blit(self.ship_image, (self.rect.x+60, self.rect.top+110))

        for btn in self.button_group:
            btn.draw(surface)
        for slot in self.equipment_slots:
            if slot.item == None and slot.type == self.state_type:
                slot.draw(surface)
        for slot in self.equipment_slots:
            if slot.item != None and slot.type == self.state_type:
                slot.rescale_item() 
                slot.draw_item(surface)

class Shop(pg.sprite.Sprite):
    def __init__(self):
            pg.sprite.Sprite.__init__(self)
            self.x = 500
            self.y = 200
            self.shop_slots = pg.sprite.Group()
            self.button_group = []

            self.button_group.append(button.Button(rect=(750,120,50,20), command = self.btn_1_pressed, picture = 'btn-left'))
            self.button_group.append(button.Button(rect=(985,120,50,20), command = self.btn_2_pressed, picture = 'btn-right'))

            self.page_state = 1

            self.image = setup.GFX['Shop-tab']
            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.top = self.y
            self.slot_id_max = 16
            
            for i in range(14):
                y = int(i/2)
                x = ((i/2)-y)*2
                self.shop_slots.add(slot.ShopSlot(i+1, self.x+149*x+248, self.y+61*y-50))
            for i in range(14):
                y = int(i/2)
                x = ((i/2)-y)*2
                self.shop_slots.add(slot.ShopSlot(i+17, self.x+149*x+248, self.y+61*y-50))


    def btn_1_pressed(self):
        self.page_state = 1
        self.slot_id_max = 16
    def btn_2_pressed(self):
        self.page_state = 2
        self.slot_id_max = 32

    def add_item(self,id,item, type):
        if type == 'misc':
            for slot in self.shop_slots:
                if slot.id == id:
                    slot.item = setup.items[item]
                    slot.item_picture = setup.items_pictures[item]
        elif type == 'Weapon':
            for slot in self.shop_slots:
                if slot.id == id:
                    slot.item = setup.weapons[item]
                    slot.item_picture = setup.weapons_pictures[item]
                    slot.item_picture = pg.transform.scale(slot.item_picture, (42,42))
        elif type == 'Armor':
            for slot in self.shop_slots:
                if slot.id == id:
                    slot.item = setup.armors[item]
                    slot.item_picture = setup.armors_pictures[item]
                    slot.item_picture = pg.transform.scale(slot.item_picture, (42,42))

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x+220, self.rect.top-100))
        for btn in self.button_group:
            btn.draw(surface)

        for slot in self.shop_slots:
            if slot.item == None and 16*(self.page_state-1) < slot.id <= self.slot_id_max:
                slot.draw(surface)
        for slot in self.shop_slots:
            if slot.item != None and 16*(self.page_state-1) < slot.id <= self.slot_id_max:
                slot.draw_item(surface)
                slot.draw_info(surface)

                
        

