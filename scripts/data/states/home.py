import pygame as pg
from scripts.data import tools, setup
from scripts.data import constant as c
from scripts import info, player, button, inventory
import pickle, gzip



class Home(tools._State):
    def __init__(self):
        tools._State.__init__(self)

    def startup(self, current_time, persist, player):
        self.game_info = persist
        self.persist = self.game_info
        self.game_info[c.CURRENT_TIME] = current_time
        self.game_info[c.LEVEL_STATE] = c.NOT_FROZEN
        self.game_info[c.PLAYER_DEAD] = False
        with gzip.open('assets\saves\savegame.txt', 'rb') as file:
            self.save_info = pickle.load(file)
        print(self.save_info)
        self.player = player
        self.shop = inventory.Shop()

        tools.keyPressed = []
        tools.keyReleased = []

        #self.overhead_info_display = info.OverheadInfo(self.game_info, c.LEVEL)

        self.inventory_pos_x = 20
        self.inventory_pos_y = 400
        self.mouse_item_carry = [0,0,0,0]
        
        
        self.setup_background()
        self.state = 'equipment'

        self.setup_shop()
    def setup_shop(self):
        self.shop.add_item(1,1,'Weapon')
        self.shop.add_item(2,2,'Weapon')
        self.shop.add_item(3,3,'Weapon')
        self.shop.add_item(4,4, 'Weapon')
        self.shop.add_item(5,5,'Weapon')
        self.shop.add_item(6,1,'Armor')

    def setup_background(self):
        self.background = setup.GFX['background'].convert()
        self.back_rect = self.background.get_rect()

        self.X1 = 0
        self.X2 = 1920
        
        width = self.back_rect.width
        height = self.back_rect.height
        self.btn_equip = button.Button(rect=(50,50,150,50), command = self.btn_equip_pressed)
        self.btn_shop = button.Button(rect=(220,50,150,50), command = self.btn_shop_pressed)
        self.btn_map = button.Button(rect=(390,50,150,50), command = self.btn_map_pressed)
    def load_game(self):
        None

    def update(self, surface, keys, current_time):
        surface.blit(self.background, (0, 0))
        
        
        self.handle_states(keys, current_time,surface)
        self.btn_equip.draw(surface)
        self.btn_shop.draw(surface)
        self.btn_map.draw(surface)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            elif event.type == pg.KEYDOWN:
                self.keys = pg.key.get_pressed()
                tools.keyPressed.append(event.key)
                print(tools.keyPressed)
            elif event.type == pg.KEYUP:
                if event.key != pg.K_LSHIFT:
                    tools.keyReleased.append(event.key)
                if event.key == pg.K_LSHIFT:
                    tools.keyPressed.remove(event.key)
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    tools.keyPressed.append("mouse")
                if event.button == 3:
                    tools.keyPressed.append("mouse2")
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    tools.keyPressed.remove("mouse")
                    tools.keyReleased.append("mouse")
                if event.button == 3:
                    if "mouse2" in tools.keyPressed:
                        tools.keyPressed.remove("mouse2")
            self.btn_equip.get_event(event)
            self.btn_shop.get_event(event)
            self.btn_map.get_event(event)
            if self.state == 'shop':
                for btn in self.shop.button_group:
                    btn.get_event(event)
            elif self.state == 'equipment':
                for btn in self.player.equipment.button_group:
                    btn.get_event(event)
    def blit_equipment(self,surface):
        self.player.player_inventory.draw(surface)
        self.player.equipment.draw(surface)
    def blit_shop(self,surface):
        self.player.player_inventory.draw(surface)
        self.shop.draw(surface)


    def handle_states(self, keys, current_time,surface):
        if self.state == 'shop':
            self.blit_shop(surface)
            if "mouse" in tools.keyReleased:
                tools.keyReleased.remove("mouse")
                for slot in self.shop.shop_slots:
                    if slot.item != None and 16*(self.shop.page_state-1) < slot.id <= self.shop.slot_id_max:
                        if slot.rect.collidepoint(pg.mouse.get_pos()):
                            for slots in self.player.player_inventory.inventory_slots:
                                if slots.item == None:
                                    slots.item = slot.item
                                    slots.item_picture = slot.item_picture
                                    self.player.inventory['gold'] -= slot.item.value*4
                                    print(self.player.inventory['gold'])
                                    break
                for slot in self.player.player_inventory.inventory_slots:
                    if slot.rect.collidepoint(pg.mouse.get_pos()) and slot.item != None:
                        if slot.item_quantity != 0:
                            self.player.inventory['gold'] += slot.item.value*slot.item_quantity
                        else:
                            self.player.inventory['gold'] += slot.item.value
                        slot.item = None
                        print(self.player.inventory['gold'])
            for slot in self.player.player_inventory.inventory_slots:
                slot.update_highlight()
            for slot in self.shop.shop_slots:
                slot.update_highlight()
        

        if self.state == 'equipment':
            self.blit_equipment(surface)
            if "mouse" not in tools.keyPressed:
                pg.mouse.get_rel()

            if "mouse" in tools.keyReleased:
                tools.keyReleased.remove("mouse")
                for slot in self.player.player_inventory.inventory_slots:
                    if slot.rect.collidepoint(pg.mouse.get_pos()) and self.mouse_item_carry[0] != 0:
                        if slot.id == self.mouse_item_carry[1]:
                            break
                        for slots in self.player.player_inventory.inventory_slots:
                            if slots.id == self.mouse_item_carry[1] and slot.item == None:
                                slots.item = None
                                slots.item_carry = False
                                slot.add_item(self.mouse_item_carry[0], self.mouse_item_carry[2], self.mouse_item_carry[3])
                                slot.item_rect.x = slot.rect.x
                                slot.item_rect.top = slot.rect.top
                                self.mouse_item_carry = [0,0,0,0]
                                pg.mouse.set_visible(True)
                                break
                            elif slots.id == self.mouse_item_carry[1] and slot.item != None:
                                slots.item_quantity = 0
                                slots.item = None
                                slots.add_item(slot.item.id, slot.item_quantity)
                                slots.item_rect.x = slots.rect.x
                                slots.item_rect.top = slots.rect.top
                                slots.item_carry = False
                                slot.item_quantity = 0
                                slot.item = None
                                slot.add_item(self.mouse_item_carry[0], self.mouse_item_carry[2], self.mouse_item_carry[3])
                                slot.item_rect.x = slot.rect.x
                                slot.item_rect.top = slot.rect.top
                                self.mouse_item_carry = [0,0,0,0]
                                pg.mouse.set_visible(True)
                                break
                for slot in self.player.player_inventory.inventory_slots:
                    if self.mouse_item_carry[0] != 0:
                        if slot.id == self.mouse_item_carry[1]:
                            slot.item_carry = False
                            slot.item_rect.x = slot.rect.x
                            slot.item_rect.top = slot.rect.top
                            self.mouse_item_carry = [0,0,0,0]
                            slot.item_picture = setup.items_pictures[slot.item.id]
                            pg.mouse.set_visible(True)
                            break
            if pg.K_e in tools.keyPressed:
                
                for slot in self.player.player_inventory.inventory_slots:
                    if slot.rect.collidepoint(pg.mouse.get_pos()):
                        if slot.item != None:
                            for slots in self.player.equipment.equipment_slots:
                                if slots.item == None and slot.item.type == slots.type:
                                    slots.add_item(slot.item.id, 0, slot.item.type)
                                    slot.item = None
                                    break
                for slot in self.player.equipment.equipment_slots:
                    if slot.rect.collidepoint(pg.mouse.get_pos()) and slot.type == self.player.equipment.state_type:
                        if slot.item != None:
                            for slots in self.player.player_inventory.inventory_slots:
                                if slots.item == None and slot.item.type == 'Weapon':
                                    slots.item = setup.weapons[slot.item.id]
                                    slots.item_picture = setup.weapons_pictures[slot.item.id]
                                    slots.item_picture = pg.transform.scale(slots.item_picture, (42,42))
                                    slots.item_grey_picture = slots.grayscale(slots.item_picture)
                                    slot.rescale_toggle = False
                                    slot.item = None
                                    break
                                elif slots.item == None and slot.item.type == 'Armor':
                                    slots.item = setup.armors[slot.item.id]
                                    slots.item_picture = setup.armors_pictures[slot.item.id]
                                    slots.item_picture = pg.transform.scale(slots.item_picture, (42,42))
                                    slots.item_grey_picture = slots.grayscale(slots.item_picture)
                                    slot.rescale_toggle = False
                                    slot.item = None
                                    break
                tools.keyPressed.remove(pg.K_e)
            if pg.K_p in tools.keyPressed:
                self.player.base_dmg = 1
                for slot in self.player.equipment.equipment_slots:
                    if slot.item != None and slot.item.type == 'Weapon':
                        self.player.base_dmg += slot.item.damage
                        slot.rescale_toggle = False
                        self.save_info['e'+str(slot.id)]['item'] = slot.item.id
                        self.save_info['e'+str(slot.id)]['type'] = slot.item.type
                    elif slot.item != None and slot.item.type == 'Armor':
                        slot.rescale_toggle = False
                        self.save_info['e'+str(slot.id)]['item'] = slot.item.id
                        self.save_info['e'+str(slot.id)]['type'] = slot.item.type
                    elif slot.item == None:
                        self.save_info['e'+str(slot.id)]['item'] = None
                        self.save_info['e'+str(slot.id)]['type'] = None
                self.save_info['credits'] = self.player.inventory['gold']
                for slot in self.player.player_inventory.inventory_slots:
                    if slot.item != None:
                        self.save_info[slot.id]['item'] = slot.item.id
                        self.save_info[slot.id]['type'] = slot.item.type
                        self.save_info[slot.id]['item_quantity'] = slot.item_quantity
                    elif slot.item == None:
                        self.save_info[slot.id]['item'] = None
                        self.save_info[slot.id]['type'] = None
                        self.save_info[slot.id]['item_quantity'] = None
                with gzip.open('assets\saves\savegame.txt', 'wb') as file:
                    pickle.dump(self.save_info, file)
                self.next = c.LEVEL1
                self.done = True

            for slot in self.player.player_inventory.inventory_slots:
                slot.update_highlight()
            for slot in self.player.equipment.equipment_slots:
                slot.update_highlight()

            if pg.K_m in tools.keyPressed:
                for slot in self.player.player_inventory.inventory_slots:
                    if slot.rect.collidepoint(pg.mouse.get_pos()):
                        if slot.item != None:
                            self.player.inventory['gold'] += slot.item.value*slot.item_quantity
                            tools.keyPressed.remove(pg.K_m)
                            slot.item_quantity = 0
                            slot.item = None

            if "mouse" in tools.keyPressed:
                for slot in self.player.player_inventory.inventory_slots:
                    if slot.rect.collidepoint(pg.mouse.get_pos()):
                        if self.player.player_inventory.check_state():
                            slot.update(3)
                        elif slot.state != c.SLOT_DEFAULT:
                            slot.update()

                    if slot.state == c.SLOT_CLICKED and slot.item != None and not slot.rect.collidepoint(pg.mouse.get_pos()):
                        tempx, tempy = pg.mouse.get_rel()
                        slot.item_rect.x += tempx
                        slot.item_rect.top += tempy
                        self.mouse_item_carry[0] = slot.item.id
                        self.mouse_item_carry[1] = slot.id
                        self.mouse_item_carry[2] = slot.item_quantity
                        self.mouse_item_carry[3] = slot.item.type
                        slot.item_picture = pg.transform.scale(slot.item_picture, (38,38))
                        slot.item_carry = True
                        pg.mouse.set_visible(False)
                        
                if self.player.player_inventory.rect.collidepoint(pg.mouse.get_pos()):
                    toggle = False
                    for slot in self.player.player_inventory.inventory_slots:
                        if slot.state != c.SLOT_DEFAULT:
                            toggle = True
                    if toggle == False:
                        tempx, tempy = pg.mouse.get_rel()
                        self.player.player_inventory.rect.x += tempx
                        self.player.player_inventory.rect.top += tempy
                        for extra in self.player.player_inventory.inventory_slots:
                            extra.rect.x += tempx
                            extra.rect.top += tempy
            if "mouse" in tools.keyReleased:
                tools.keyReleased.remove("mouse")
            if "mouse2" in tools.keyPressed:
                tools.keyPressed.remove("mouse2")

    def btn_equip_pressed(self):
        self.state = 'equipment'
    def btn_shop_pressed(self):
        self.state = 'shop'
    def btn_map_pressed(self):
        self.state = 'map'


        