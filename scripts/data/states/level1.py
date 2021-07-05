from __future__ import division

import pygame as pg
from scripts.data import setup, tools
from scripts.data import constant as c
from scripts import player
from scripts import info
from scripts import enemy
from scripts import powerup
from scripts import shield
import random
from scripts import score
import math
import pickle
import gzip

class Level1(tools._State):
    def __init__(self):
        tools._State.__init__(self)

    def startup(self, current_time, persist, player):
        self.game_info = persist
        self.persist = self.game_info
        self.game_info[c.CURRENT_TIME] = current_time
        self.game_info[c.LEVEL_STATE] = c.NOT_FROZEN
        self.game_info[c.PLAYER_DEAD] = False
        self.save_info = {'credits':0,
                                   1:{'item' : 1,
                                                            'type' : 'misc',
                                                            'item_quantity':50},
                                       
                                                        2:{},3:{},4:{},5:{},6:{},7:{},8:{},9:{},10:{},11:{},12:{},13:{},14:{},15:{},16:{},17:{},18:{},
                                                        19:{},20:{},21:{},22:{},23:{},24:{},25:{},26:{},27:{},28:{},29:{},30:{},31:{},32:{}
            }
        self.player = player

        tools.keyPressed = []
        tools.keyReleased = []

        self.state = c.NOT_FROZEN
        self.inventory_toggle = False
        self.level = self.game_info[c.LEVEL]
        self.death_timer = 0
        self.spawn_timer = 0
        self._timer = 0
        self.moving_score_list = []
        self.overhead_info_display = info.OverheadInfo(self.game_info, c.LEVEL)
        self.mouse_pos = {'x':0,
                                    'y':0}
        self.inventory_pos_x = 20
        self.inventory_pos_y = 400
        self.mouse_item_carry = [0,0,0,0]
        
        
        self.setup_background()
        self.setup_player()
        self.setup_spritegroups()
        self.setup_cursor()
        self.create_option_ui()
        

        
        

    def setup_background(self):
        self.background = setup.GFX['background'].convert()
        self.back_rect = self.background.get_rect()

        self.X1 = 0
        self.X2 = 1920
        
        width = self.back_rect.width
        height = self.back_rect.height
    def setup_player(self):
        #try:
            self.game_load()
        #except:
           # self.game_new()
    def game_load(self):

        with gzip.open('assets\saves\savegame.txt', 'rb') as file:
            self.save_info = pickle.load(file)


        self.player.inventory['gold'] = self.save_info['credits']
        self.player.base_dmg = 1
        for slot in self.player.equipment.equipment_slots:
            if self.save_info['e'+str(slot.id)]['item'] != None:
                #if self.save_info['e'+str(slot.id)]['type'] == 'Weapon' and slot.type == 'Weapon':
                    slot.add_item(self.save_info['e'+str(slot.id)]['item'],0,self.save_info['e'+str(slot.id)]['type'])
                    if slot.item != None and slot.type == 'Weapon':
                        self.player.base_dmg += slot.item.damage

        #Fixa det här för det är duplicer
        for slot in self.player.player_inventory.inventory_slots:
            if self.save_info[slot.id]['item'] != None:
                if self.save_info[slot.id]['type'] == 'misc':
                    slot.add_item(self.save_info[slot.id]['item'], self.save_info[slot.id]['item_quantity'], 'misc')
                    slot.item_quantity = self.save_info[slot.id]['item_quantity']
                elif self.save_info[slot.id]['type'] == 'Weapon':
                    slot.item = setup.weapons[self.save_info[slot.id]['item']]
                    slot.item_picture = setup.weapons_pictures[self.save_info[slot.id]['item']]
                    slot.item_picture = pg.transform.scale(slot.item_picture, (42,42))
                    slot.item_grey_picture = slot.grayscale(slot.item_picture)
                elif self.save_info[slot.id]['type'] == 'Armor':
                    slot.item = setup.armors[self.save_info[slot.id]['item']]
                    slot.item_picture = setup.armors_pictures[self.save_info[slot.id]['item']]
                    slot.item_picture = pg.transform.scale(slot.item_picture, (42,42))
                    slot.item_grey_picture = slot.grayscale(slot.item_picture)
        self.player.rect.x = 110
        self.player.rect.bottom = 200
       
    def game_new(self):
        self.player = player.Player(self.save_info)
        self.player.rect.x = 110
        self.player.rect.bottom = 200
        print(self.save_info)
        

    def setup_spritegroups(self):
        self.enemy_group = pg.sprite.Group()
        self.powerup_group = pg.sprite.Group()
        self.bullet_group = pg.sprite.Group()
        self.shield_group = pg.sprite.Group()
        self.drone_group = pg.sprite.Group()

        

        self.player_and_enemy_group = pg.sprite.Group(self.player)

    def update(self, surface, keys, current_time):
        """Updates Entire level using states.  Called by the control object"""

        
        self.game_info[c.CURRENT_TIME] = self.current_time = current_time
        self.handle_states(keys, current_time)
        if self.state == c.NOT_FROZEN:
            self.blit_everything(surface)
        elif self.state == c.PAUSED:
            self.blit_everything_options(surface)
        if self.inventory_toggle:
            self.player.player_inventory.draw(surface)
        self.save_info_saver()
        
    def save_info_saver(self):
        self.save_info['credits'] = self.player.inventory['gold']
        for slot in self.player.equipment.equipment_slots:
            if slot.item != None:
                self.save_info['e'+str(slot.id)]['item'] = slot.item.id
                self.save_info['e'+str(slot.id)]['type'] = slot.item.type
            elif slot.item == None:
                self.save_info['e'+str(slot.id)]['item'] = None
                self.save_info['e'+str(slot.id)]['type'] = None
        for slot in self.player.player_inventory.inventory_slots:
            if slot.item != None:
                
                self.save_info[slot.id]['item'] = slot.item.id
                self.save_info[slot.id]['type'] = slot.item.type
                self.save_info[slot.id]['item_quantity'] = slot.item_quantity
            elif slot.item == None:
                self.save_info[slot.id]['item'] = None
                self.save_info[slot.id]['type'] = None
                self.save_info[slot.id]['item_quantity'] = None
                


    def handle_states(self, keys, current_time):
        if pg.QUIT in tools.keyEvent:
            self.save_game()
            pg.quit()
            tools.keyEvent.remove(pg.QUIT)
        if pg.K_p in tools.keyPressed:
            if self.state == c.NOT_FROZEN:
                self.state = c.PAUSED
            elif self.state == c.PAUSED:
                self.state = c.NOT_FROZEN
            tools.keyPressed.remove(pg.K_p)
        if self.state == c.NOT_FROZEN:
            if tools.keybinding['up'] in tools.keyPressed:
                self.player.y_vel -= self.player.speed
                tools.keyPressed.remove(tools.keybinding['up'])
            if tools.keybinding['down'] in tools.keyPressed:
                self.player.y_vel += self.player.speed
                tools.keyPressed.remove(tools.keybinding['down'])
            if tools.keybinding['right'] in tools.keyPressed:
                self.player.x_vel += self.player.speed
                tools.keyPressed.remove(tools.keybinding['right'])
            if tools.keybinding['left'] in tools.keyPressed:
                self.player.x_vel -= self.player.speed
                tools.keyPressed.remove(tools.keybinding['left'])
            if pg.K_i in tools.keyPressed:
                if self.inventory_toggle == False:
                    self.inventory_toggle = True
                else:
                    self.inventory_toggle = False
                tools.keyPressed.remove(pg.K_i)
            if pg.K_LSHIFT in tools.keyPressed:
                if pg.K_1 in tools.keyPressed:
                    self.player.ammo = self.player.ammo_t1
                    tools.keyPressed.remove(pg.K_1)
                if pg.K_2 in tools.keyPressed:
                    self.player.ammo = self.player.ammo_t2
                    tools.keyPressed.remove(pg.K_2)
                if pg.K_3 in tools.keyPressed:
                    self.player.ammo = self.player.ammo_tier_GOD
                    tools.keyPressed.remove(pg.K_3)
            if pg.K_c in tools.keyPressed:
                if self.player.shield_active == False:
                    if self.player.current_shield > 0:
                        self.player.create_shield(self.shield_group)
                elif self.player.shield_active == True:
                    self.shield_group.remove(self.player.shield)
                    self.player.shield_active = False
                tools.keyPressed.remove(pg.K_c)
            if pg.K_1 in tools.keyPressed:
                self.player.weapon = 'Blaster'
                self.player.inventory[self.player.ammo_t1.name] += 1000
                self.player.credits -= 100
                tools.keyPressed.remove(pg.K_1)
            if pg.K_2 in tools.keyPressed:
                self.player.weapon = 'Dual Blaster'
                tools.keyPressed.remove(pg.K_2)
            if pg.K_3 in tools.keyPressed:
                self.player.weapon = 'Shotgun'
                tools.keyPressed.remove(pg.K_3)
            if pg.K_r in tools.keyPressed:
                self.player.shoot_rockets(self.powerup_group)
                tools.keyPressed.remove(pg.K_r)
            if tools.keybinding['up'] in tools.keyReleased:
                self.player.y_vel += self.player.speed
                tools.keyReleased.remove(tools.keybinding['up'])
            if tools.keybinding['down'] in tools.keyReleased:
                self.player.y_vel -= self.player.speed
                tools.keyReleased.remove(tools.keybinding['down'])
            if tools.keybinding['right'] in tools.keyReleased:
                self.player.x_vel -= self.player.speed
                tools.keyReleased.remove(tools.keybinding['right'])
            if tools.keybinding['left'] in tools.keyReleased:
                self.player.x_vel += self.player.speed
                tools.keyReleased.remove(tools.keybinding['left'])


            self.mouse_pos['x'], self.mouse_pos['y'] = pg.mouse.get_pos()
            if "mouse" not in tools.keyPressed:
                pg.mouse.get_rel()

            if "mouse" in tools.keyReleased and self.inventory_toggle == True:
                tools.keyReleased.remove("mouse")
                for slot in self.player.player_inventory.inventory_slots:
                    if slot.rect.collidepoint(pg.mouse.get_pos()) and self.mouse_item_carry[0] != 0:
                        if slot.id == self.mouse_item_carry[1]:
                            break
                        for slots in self.player.player_inventory.inventory_slots:
                            if slots.id == self.mouse_item_carry[1] and slot.item == None:
                                slots.item = None
                                slots.item_carry = False
                                slots.item_rect.x = slots.rect.x
                                slots.item_rect.top = slots.rect.top
                                slot.add_item(self.mouse_item_carry[0], self.mouse_item_carry[2], self.mouse_item_carry[3])
                                slot.item_rect.x = slot.rect.x
                                slot.item_rect.top = slot.rect.top
                                self.mouse_item_carry = [0,0,0,0]
                                pg.mouse.set_visible(True)
                                break
                            elif slots.id == self.mouse_item_carry[1] and slot.item != None:
                                slots.item_quantity = 0
                                slots.item = None
                                slots.item_rect.x = slots.rect.x
                                slots.item_rect.top = slots.rect.top
                                slots.add_item(slot.item.id, slot.item_quantity, slot.item.type)
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


            if self.inventory_toggle == True:
                for slot in self.player.player_inventory.inventory_slots:

                   
                        for slot in self.player.player_inventory.inventory_slots:
                            if slot.rect.collidepoint(pg.mouse.get_pos()):
                                slot.update(2)
                            elif slot.state != c.SLOT_DEFAULT and "mouse" not in tools.keyPressed:
                                slot.update()

            if pg.K_m in tools.keyPressed and self.inventory_toggle == True:
                for slot in self.player.player_inventory.inventory_slots:
                    if slot.rect.collidepoint(pg.mouse.get_pos()):
                        if slot.item != None:
                            self.player.inventory['gold'] += slot.item.value*slot.item_quantity+1
                            tools.keyPressed.remove(pg.K_m)
                            slot.item_quantity = 0
                            slot.item = None

            if "mouse" in tools.keyPressed and self.inventory_toggle == True:

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
            

        if self.state == c.NOT_FROZEN:
            self.update_all_sprites(keys)
            self.update_background()
            self.check_for_player_death()
            self.level_designer(current_time)
        elif self.state == c.GAME_OVER:
            self.end_game()
        elif self.state == c.PAUSED:
            
            if tools.keybinding['up'] in tools.keyPressed:
                if self.cursor.state == c.SPACE:
                    self.cursor.rect.y = 273
                    self.cursor.state = c.RESUME
                elif self.cursor.state == c.HOME:
                    self.cursor.rect.y = 330
                    self.cursor.state = c.SPACE
                tools.keyPressed.remove(tools.keybinding['up'])
            if tools.keybinding['down'] in tools.keyPressed:
                if self.cursor.state == c.RESUME:
                    self.cursor.rect.y = 330
                    self.cursor.state = c.SPACE
                elif self.cursor.state == c.SPACE:
                    self.cursor.rect.y = 387
                    self.cursor.state = c.HOME
                tools.keyPressed.remove(tools.keybinding['down'])
            if tools.keybinding['enter'] in tools.keyPressed:
                if self.cursor.state == c.RESUME:
                    self.state = c.NOT_FROZEN
                if self.cursor.state == c.HOME:
                    self.save_game()
                    self.next = c.MAIN_MENU
                    self.done = True
                if self.cursor.state == c.SPACE:
                    self.next = c.HOME
                    self.save_game()
                    self.done = True
                   
                tools.keyPressed.remove(tools.keybinding['enter'])
        elif self.state == c.VICTORY:
            self.update_while_winning()


            
            


    def setup_cursor(self):
        """Skapar cursorn"""
        self.cursor = pg.sprite.Sprite()
        dest = (446, 273)
        self.cursor.image, self.cursor.rect = self.get_image(0, 0, 72, 22, dest, setup.GFX['ui-options-cursor'])
        self.cursor.state = c.RESUME
    def create_option_ui(self):
        self.option_ui = pg.sprite.Sprite()
        dest = (400, 120)
        self.option_ui.image, self.option_ui.rect = self.get_image(0, 0, 100, 150, dest, setup.GFX['ui-options'])
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
    def level_designer(self,current_time):
        if self.level == c.LEVEL_1:
            self.level_1(current_time)
    def level_1(self, current_time):
        if self.spawn_timer == 0:
            self.spawn_timer = current_time
        elif current_time - self.spawn_timer > 5000:
            rng = random.randint(1,255)
            if rng < 250:
                for i in range(1):
                    self.enemy_group.add(enemy.Explorer())
            elif rng >250:
                self.enemy_group.add(enemy.Explorer_BOSS())

                
            elif rng > 255:
                for i in range(3):
                    self.enemy_group.add(enemy.Seeker())

            self.spawn_timer = 0

    def update_all_sprites(self, keys):
        self.player.update(keys, self.game_info, self.powerup_group)
        self.enemy_group.update(self.game_info, self.powerup_group, self.player)
        self.shield_group.update(self.player)
        self.check_for_player_death()
        self.adjust_sprite_positions()
        self.overhead_info_display.update(self.game_info, self.player, self.current_time)
        for score in self.moving_score_list:
            score.update(self.moving_score_list, self.game_info)

    def update_background(self):
        self.X1 -= 1.4
        self.X2 -= 1.4

        if self.X1 < -1920:
            self.X1 = 1920
        if self.X2  < -1920:
            self.X2 = 1920

    def adjust_sprite_positions(self):
        """Adjusts sprites by their x and y velocities and collisions"""
        self.adjust_player_position()
        self.adjust_enemy_position()
        self.adjust_powerup_position()

    def adjust_player_position(self):
        self.last_x_position = self.player.rect.x
        self.last_y_position = self.player.rect.bottom
        self.player.rect.x += self.player.x_vel
        self.player.rect.y += self.player.y_vel

        if self.player.rect.x < 0 or self.player.rect.x > c.SCREEN_WIDTH or self.player.rect.bottom > c.SCREEN_HEIGHT-10 or self.player.rect.bottom < 10:
            self.player.health -= 1
        self.save_info['credits'] = self.player.credits
        self.check_player_collisions()

    def check_player_collisions(self):
        enemy = pg.sprite.spritecollideany(self.player, self.enemy_group)

        

        powerup = pg.sprite.spritecollideany(self.player, self.powerup_group)

        
        if enemy:
            if enemy.state == c.FLYING:
                enemy.transition_death()
                self.player.health -= 1
        elif powerup:
            if powerup.name == c.ATK_LVL_1:
                self.game_info[c.SCORE] += 1000
                self.player.damage += 1

            elif powerup.name == c.HEART_LVL_1:
                self.game_info[c.SCORE] += 5000
                if self.player.health < self.player.max_health:
                    self.player.health += 1
                    self.moving_score_list.append(
                    score.Score(powerup.rect.right,
                                powerup.rect.y, 1, 'green'))
            elif powerup.name == c.COIN:
                #setup.SFX['coin_pickup'].play()
                self.moving_score_list.append(
                    score.Score(powerup.rect.right,
                                powerup.rect.y, powerup.value, 'white'))
                self.player.inventory['gold'] += powerup.value
                powerup.kill()
                #print(self.save_info)
            elif powerup.name == c.ENEMY_LASER:
                self.player.health -= powerup.dmg
                self.moving_score_list.append(
                    score.Score(powerup.rect.right,
                                powerup.rect.y, powerup.dmg, 'red'))
                powerup.kill()
            if powerup.name != c.LASER and powerup.name != c.COIN and powerup.name != 'rocket' and powerup.name != 'Shotgun':
                powerup.kill()

    def adjust_enemy_position(self):
        """Moves all enemies along the x, y axes and check for collisions"""
        for enemy in self.enemy_group:
            if enemy.name == 'Explorer' or enemy.name == 'Viper':
                enemy.rect.x += enemy.x_vel
                enemy.rect.y += enemy.y_vel
            elif enemy.name == 'Seeker':
                directionX = self.player.rect.x - enemy.rect.x
                directionY = self.player.rect.y - enemy.rect.y
                hyp = math.sqrt(directionX*directionX + directionY*directionY)

                if hyp != 0:
                    directionX /= hyp
                    directionY /= hyp
                if hyp < 50:
                    if enemy.died != True:
                        self.player.health -= enemy.dmg
                        self.moving_score_list.append(
                            score.Score(enemy.rect.right,
                                        enemy.rect.y, enemy.dmg, 'red'))
                        enemy.transition_death()

                enemy.rect.x += directionX*5
                enemy.rect.y += directionY*5


    def adjust_powerup_position(self):
        """lasers along the x, y axes"""
        for powerup in self.powerup_group:
            if powerup.name == c.HEART_LVL_1:
                self.adjust_heart_position(powerup)
            elif powerup.name == c.ATK_LVL_1:
                self.adjust_atkboost_position(powerup)
            elif powerup.name == c.COIN:
                self.adjust_coin_position(powerup)
            elif powerup.name == c.LASER or powerup.name == c.ENEMY_LASER or powerup.name == 'rocket'or powerup.name == 'Shotgun':
                self.adjust_laser_position(powerup)
                powerup.update(self.game_info)



    def adjust_heart_position(self, heart):


        directionX = self.player.rect.x - heart.rect.x
        directionY = self.player.rect.y - heart.rect.y

        hyp = math.sqrt(directionX*directionX + directionY*directionY)
        
        if hyp != 0:
            directionX /= hyp
            directionY /= hyp

        if hyp < 100:
            heart.rect.x += directionX*5
            heart.rect.y += directionY*5
        else:
            heart.rect.x += heart.x_vel
            heart.rect.y += heart.y_vel
    def adjust_atkboost_position(self, atkboost):
        atkboost.rect.x += atkboost.x_vel
        atkboost.rect.y += atkboost.y_vel
    def adjust_laser_position(self, laser):
        """Moves fireball along the x, y axes and checks for collisions"""
        laser.rect.x += laser.x_vel
        laser.rect.y += laser.y_vel
        if laser.name == c.LASER or laser.name == 'rocket'or laser.name == 'Shotgun':
            self.check_laser_x_collisions(laser)
        elif laser.name == c.ENEMY_LASER:
            self.check_enemylaser_x_collisions(laser)
    def adjust_coin_position(self, coin):
        directionX = self.player.rect.x - coin.rect.x
        directionY = self.player.rect.y - coin.rect.y

        hyp = math.sqrt(directionX*directionX + directionY*directionY)
        
        if hyp != 0:
            directionX /= hyp
            directionY /= hyp

        if hyp < 250:
            coin.rect.x += directionX*12
            coin.rect.y += directionY*12



        coin.update(self.game_info)
    def check_enemylaser_x_collisions(self, laser):
        if laser.rect.x > c.SCREEN_WIDTH or laser.rect.x < 0:
            laser.kill()
        if self.player.shield_active == True:
            shield = pg.sprite.spritecollideany(laser, self.shield_group)
            if shield:
                self.player.current_shield -= laser.dmg
                laser.kill()
                if self.player.current_shield  < 1:
                    self.player.shield_active = False
                    self.shield_group.remove(self.player.shield)
    def check_laser_x_collisions(self, laser):
        
        if laser.rect.x > c.SCREEN_WIDTH or laser.rect.x < -50:
            laser.kill()

        enemy = pg.sprite.spritecollideany(laser, self.enemy_group)
        
        if enemy and laser.name != 'rocket':
            if laser.hit == False and enemy.died == False: 
                if laser.name == c.LASER:
                    self.moving_score_list.append(
                        score.Score(laser.rect.right,
                                    laser.rect.y, self.player.dmg, 'red'))
                    self.laser_kill(laser, enemy)
                    laser.hit = True
                elif laser.name == 'Shotgun':
                    self.moving_score_list.append(
                        score.Score(laser.rect.right,
                                    laser.rect.y, self.player.shotgun_dmg, 'red'))
                    self.laser_kill(laser, enemy, self.player.shotgun_dmg)
                    laser.hit = True
        if laser.name == 'rocket':
            for enemy in self.enemy_group:
                directionX = enemy.rect.centerx - laser.rect.x
                directionY = enemy.rect.centery - laser.rect.y

                hyp = math.sqrt(directionX*directionX + directionY*directionY)

                if hyp != 0:
                    directionX /= hyp
                    directionY /= hyp
                if hyp < 15:
                    if laser.hit == False and enemy.died == False:

                        
                        laser.hit = True
                        for enemies in self.enemy_group:
                            directionX2 = enemies.rect.centerx - laser.rect.x
                            directionY2 = enemies.rect.centery - laser.rect.y

                            hip = math.sqrt(directionX2*directionX2+ directionY2*directionY2)

                            if abs(hip) < 150:
                                self.moving_score_list.append(
                                    score.Score(enemy.rect.right,
                                    enemy.rect.y, self.player.rocket_dmg, 'red'))
                                self.laser_kill(laser, enemies, self.player.rocket_dmg)

                if hyp < 150 and directionX > 0 :
                    if enemy.died == False and laser.hit == False:
                        laser.rect.x += directionX*12
                        laser.rect.y += directionY*15
                        return
                    elif laser.hit == False:
                        laser.x_vel = 12
                elif laser.hit == False:
                    laser.x_vel = 12
    def laser_kill(self, laser, enemy, dmg = 1):
        self.game_info[c.SCORE] += (100 + random.randint(1,500))
        if dmg == 1:
            dmg_done = laser.damage
        else:
            dmg_done = dmg
       
        if enemy.state == c.FLYING:
            enemy.current_health -= dmg_done
            if enemy.current_health <= 0:
                
                enemy.transition_death()
            laser.hit_transition()

    def delete_if_off_screen(self, enemy):
        """Removes enemy from sprite groups if 500 pixels left off the screen,
         underneath the bottom of the screen"""
        if enemy.rect.x < -50:
            enemy.kill()
    def check_for_player_death(self):
        if self.player.health < 1:
            self.player.dead = True
            self.game_info[c.PLAYER_DEAD] = True
            self.state = c.GAME_OVER
    def end_game(self):
        """End the game with a victory"""
        if self._timer == 0:
            self._timer = self.current_time
            self.save_game()
        elif (self.current_time - self._timer) > 2000:
            self.next = c.MAIN_MENU
            self.done = True
    def save_game(self):
         with gzip.open('assets\saves\savegame.txt', 'wb') as file:
            pickle.dump(self.save_info, file)

    def blit_everything(self, surface):
        #Blit all sprites to the main surface

        
        surface.blit(self.background, (0, 0))
        #surface.blit(self.background, (self.X2, 0))
       
        self.player_and_enemy_group.draw(surface)
        self.shield_group.draw(surface)
        self.enemy_group.draw(surface)
        self.powerup_group.draw(surface)
        self.overhead_info_display.draw(surface)
        
        for score in self.moving_score_list:
            score.draw(surface)

    
    def blit_everything_options(self, surface):
        
        

        surface.blit(self.option_ui.image, (self.option_ui.rect.x, self.option_ui.rect.y))
        surface.blit(self.cursor.image, (self.cursor.rect.x, self.cursor.rect.y))





            




    
    