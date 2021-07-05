#! python3
import pygame as pg
import random
from scripts.data import setup, coin_drop
from scripts.data import constant as c
from scripts import powerup




class Enemy(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        

    def setup_enemy(self, x, y, name, setup_frame):
        self.sprite_sheet = setup.GFX['Explorer']
        self.frames = []
        self.frame_index = 0
        self.animate_timer = 0
        self.death_timer = 0
        self.shoot_timer = 0
        self.state = c.FLYING
        self.died = False

        self.name = name
        

        self.setup_frames()
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        

        self.x_vel = -1
        self.y_vel = 0



    def get_image(self, x, y, width, height):
        """Get the image frames from the sprite sheet"""
        image = pg.Surface([width, height]).convert()
        rect = image.get_rect()

        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(c.BLACK)


        image = pg.transform.scale(image,
                                   (int(rect.width*1.3),
                                    int(rect.height*1.3)))
        return image

    def handle_state(self, powerup_group):
        if self.state == c.FLYING:
            self.flying()
        if self.state == c.PLAYER_DEAD:
            self.dying(powerup_group)
        
    def animation(self):
        """Basic animation, switching between two frames"""
        self.image = self.frames[self.frame_index]

    def update(self, game_info, powerup_group, player = None):
        """Updates enemy behavior"""
        self.current_time = game_info[c.CURRENT_TIME]
        self.handle_state(powerup_group, player)
        self.animation()

class Explorer(Enemy):
    def __init__(self, x = c.SCREEN_WIDTH, y = None, name = 'Explorer'): 
        Enemy.__init__(self)
        self.y1 = random.randint(50,450)
        self.setup_enemy(x, self.y1, name, self.setup_frames) 
        self.dmg = 10
        self.max_health = 25
        self.current_health = 25
        self.drop_money = random.randint(5,10)
        self.drop_table = [1,2,3,4,5,1,2,1]
        self.drop_chance = [1000,100,50,25,5,100,20,1000]
        self.drop_type = ['misc','misc','misc','misc','misc', 'Weapon','Weapon','Armor']
        self.drop_amount_low = [3,2,1,1,1,1,1,1]
        self.drop_amount_high = [6,4,1,1,1,1,1,1]
        

    def setup_frames(self):
        self.frames.append(
            self.get_image(0,0,32,21))
        self.frames.append(
            self.get_image(32,0, 32, 21))
        self.frames.append(
            self.get_image(64,0, 32, 21))
        self.frames.append(
            self.get_image(96, 0, 32, 22))
        self.frames.append(
            self.get_image(128,0,32,22))
        self.frames.append(
            self.get_image(160,0,32,22))
        self.frames.append(
            self.get_image(192,0,32,22))
    def handle_state(self, powerup_group, player):
        if self.state == c.FLYING:
            self.flying(powerup_group)
        if self.state == c.PLAYER_DEAD:
            self.dying(powerup_group, player)


    def flying(self, powerup_group):
        if (self.current_time - self.animate_timer) > 250:
            if self.frame_index <= 1:
                self.frame_index += 1
            elif self.frame_index == 2:
                self.frame_index = 0

            self.animate_timer = self.current_time
        self.check_to_allow_laser(powerup_group)

    def dying(self,powerup_group, player):
        if self.current_time - self.animate_timer > 200:
            if self.frame_index <= 5:
                self.frame_index += 1
                self.animate_timer = self.current_time
            elif self.current_time - self.animate_timer > 200:
                self.kill()
                powerup_group.add(powerup.Coin(self.rect.x, self.rect.y, self.drop_money))
                for drop in range(len(self.drop_table)):
                    if self.drop_chance[drop] > random.randint(1,1000):
                        if self.drop_type[drop] == 'misc':
                            player.player_inventory.add_item_to_slot(self.drop_table[drop], random.randint(self.drop_amount_low[drop], self.drop_amount_high[drop]), self.drop_type[drop])
                        elif self.drop_type[drop] == 'Weapon':
                            for slot in player.player_inventory.inventory_slots:
                                if slot.item == None:
                                    slot.item = setup.weapons[self.drop_table[drop]]
                                    slot.item_picture = pg.transform.scale(setup.weapons_pictures[self.drop_table[drop]], (42,42))
                                    slot.item_grey_picture = slot.grayscale(slot.item_picture)
                                    break
                        elif self.drop_type[drop] == 'Armor':
                            for slot in player.player_inventory.inventory_slots:
                                if slot.item == None:
                                    slot.item = setup.armors[self.drop_table[drop]]
                                    slot.item_picture = pg.transform.scale(setup.armors_pictures[self.drop_table[drop]],(42,42))
                                    slot.item_grey_picture = slot.grayscale(slot.item_picture)
                                    break
                            
                
                if random.randint(1,100) > 85:

                    powerup_group.add(powerup.Heart(self.rect.x, self.rect.y))

    def check_to_allow_laser(self, group):
        """Check to allow the shooting of a laser"""
        if self.shoot_timer == 0:
            
            self.shoot_timer = self.current_time
        elif self.current_time - self.shoot_timer > 2500:
            self.shoot_laser(group)
            self.shoot_timer = self.current_time
        else:
            pass
        

    def shoot_laser(self,powerup_group):
        #setup.SFX['laser_sound_effect'].play()
        

        powerup_group.add(powerup.Enemy_Laser(self.rect.left, self.rect.y +15, self.dmg))


    def transition_death(self):
            
        #gör om laserns state till prick state om den prickar något
        self.frame_index = 3
        #centerx = self.rect.centerx
        self.image = self.frames[self.frame_index]
        self.x_vel = 0
        #self.rect.centerx = centerx
        self.state = c.PLAYER_DEAD
        self.died = True
class Explorer_BOSS(Enemy):
    def __init__(self, x = c.SCREEN_WIDTH-200, y = None, name = 'ExplorerBOSS'): 
        Enemy.__init__(self)
        self.y1 = random.randint(50,450)
        self.setup_enemy(x, self.y1, name, self.setup_frames) 
        self.dmg = 50
        self.max_health = 2500
        self.current_health = 2500
        self.x_vel =  0
        self.drop_money = random.randint(1200000,2500000)
        self.drop_table = [5,1,1, 2,3,4,5,3]
        self.drop_chance = [100,500,1000, 200, 100,50,10,200]
        self.drop_type = ['misc','Weapon','misc', 'Weapon','Weapon','Weapon','Weapon','misc']
        self.drop_amount_low = [1,1,20,1,1,1,1,3]
        self.drop_amount_high = [1,1,50,1,1,1,1,5]
        

    def setup_frames(self):
        self.frames.append(
            self.get_image(0,0,32,21))
        self.frames.append(
            self.get_image(32,0, 32, 21))
        self.frames.append(
            self.get_image(64,0, 32, 21))
        self.frames.append(
            self.get_image(96, 0, 32, 22))
        self.frames.append(
            self.get_image(128,0,32,22))
        self.frames.append(
            self.get_image(160,0,32,22))
        self.frames.append(
            self.get_image(192,0,32,22))
        index = 0
        
        for image in self.frames:
            rect = image.get_rect()
            image = pg.transform.scale(image,
                                   (int(rect.width*4),
                                    int(rect.height*4)))
            self.frames[index] = image
            index += 1
    def dying(self,powerup_group, player):
        if self.current_time - self.animate_timer > 200:
            if self.frame_index <= 5:
                self.frame_index += 1
                self.animate_timer = self.current_time
            elif self.current_time - self.animate_timer > 200:
                self.kill()
                powerup_group.add(powerup.Coin(self.rect.x, self.rect.y, self.drop_money))
                for drop in range(len(self.drop_table)):
                    if self.drop_chance[drop] > random.randint(1,1000):
                        if self.drop_type[drop] == 'misc':
                            player.player_inventory.add_item_to_slot(self.drop_table[drop], random.randint(self.drop_amount_low[drop], self.drop_amount_high[drop]), self.drop_type[drop])
                        elif self.drop_type[drop] == 'Weapon':
                            for slot in player.player_inventory.inventory_slots:
                                if slot.item == None:
                                    slot.item = setup.weapons[self.drop_table[drop]]
                                    slot.item_picture = setup.weapons_pictures[self.drop_table[drop]]
                                    slot.item_grey_picture = slot.grayscale(slot.item_picture)
                                    break
                            
                
                if random.randint(1,100) > 85:

                    powerup_group.add(powerup.Heart(self.rect.x, self.rect.y))
    def handle_state(self, powerup_group, player):
        if self.state == c.FLYING:
            self.flying(powerup_group)
        if self.state == c.PLAYER_DEAD:
            self.dying(powerup_group, player)

    def flying(self, powerup_group):
        if (self.current_time - self.animate_timer) > 250:
            if self.frame_index <= 1:
                self.frame_index += 1
            elif self.frame_index == 2:
                self.frame_index = 0

            self.animate_timer = self.current_time
        self.check_to_allow_laser(powerup_group)

    def check_to_allow_laser(self, group):
        """Check to allow the shooting of a laser"""
        if self.shoot_timer == 0:
            
            self.shoot_timer = self.current_time
        elif self.current_time - self.shoot_timer > 2500:
            self.shoot_laser(group)
            self.shoot_timer = self.current_time
        else:
            pass
        

    def shoot_laser(self,powerup_group):
        #setup.SFX['laser_sound_effect'].play()
        

        powerup_group.add(powerup.Enemy_Laser(self.rect.left, self.rect.y +15, self.dmg))


    def transition_death(self):
            
        #gör om laserns state till prick state om den prickar något
        self.frame_index = 3
        #centerx = self.rect.centerx
        self.image = self.frames[self.frame_index]
        self.x_vel = -1
        #self.rect.centerx = centerx
        self.state = c.PLAYER_DEAD
        self.died = True

class Viper(Enemy):
    def __init__(self, x = c.SCREEN_WIDTH-100, y = None, name = 'Viper'): 
        Enemy.__init__(self)
        self.y1 = random.randint(50,450)
        self.setup_enemy(x, self.y1, name, self.setup_frames) 
        self.dmg = 100
        self.max_health = 40000
        self.current_health = 40000
        self.drop_money = random.randint(100_000_00,200_000_00)
        self.drop_table = [5]
        self.drop_chance = [400]
        self.drop_type = ['Weapon']
        self.drop_amount_low = [1]
        self.drop_amount_high = [1]
        self.x_vel = 0
        self.move_timer = 0

    def setup_frames(self):
        self.frames.append(setup.GFX['Enemy_Viper'])
        self.frames[0].set_colorkey((255,255,255))
    def handle_state(self, powerup_group, player):
        if self.state == c.FLYING:
            self.flying(powerup_group,player)
        if self.state == c.PLAYER_DEAD:
            self.dying(powerup_group, player)


    def flying(self, powerup_group,player):
        self.check_to_allow_laser(powerup_group)
        self.check_if_move(player)
    def check_if_move(self, player):

        if self.current_time-self.move_timer > 1000 and self.current_time-self.move_timer < 1500:
            self.x_vel = -1
        elif self.current_time-self.move_timer > 1500:
            self.move_timer = self.current_time
            self.x_vel = 0

    def dying(self,powerup_group, player):
                self.kill()
                powerup_group.add(powerup.Coin(self.rect.x, self.rect.y, self.drop_money))
                for drop in range(len(self.drop_table)):
                    if self.drop_chance[drop] > random.randint(1,1000):
                        if self.drop_type[drop] == 'misc':
                            player.player_inventory.add_item_to_slot(self.drop_table[drop], random.randint(self.drop_amount_low[drop], self.drop_amount_high[drop]), self.drop_type[drop])
                        elif self.drop_type[drop] == 'Weapon':
                            for slot in player.player_inventory.inventory_slots:
                                if slot.item == None:
                                    slot.item = setup.weapons[self.drop_table[drop]]
                                    slot.item_picture = setup.weapons_pictures[self.drop_table[drop]]
                                    slot.item_picture = pg.transform.scale(slot.item_picture, (42,42))
                                    slot.item_grey_picture = slot.grayscale(slot.item_picture)
                                    break
                if random.randint(1,100) > 85:
                    powerup_group.add(powerup.Heart(self.rect.x, self.rect.y))

    def check_to_allow_laser(self, group):
        """Check to allow the shooting of a laser"""
        if self.shoot_timer == 0:
            
            self.shoot_timer = self.current_time
        elif self.current_time - self.shoot_timer > 1000:
            self.shoot_laser(group)
            self.shoot_timer = self.current_time
        else:
            pass
        

    def shoot_laser(self,powerup_group):
        #setup.SFX['laser_sound_effect'].play()
        

        powerup_group.add(powerup.Enemy_Laser(self.rect.left, self.rect.y +15, self.dmg,'Viper_laser'))
        powerup_group.add(powerup.Enemy_Laser(self.rect.left, self.rect.y, self.dmg,'Viper_laser'))


    def transition_death(self):
            

        self.x_vel = 0
        #self.rect.centerx = centerx
        self.state = c.PLAYER_DEAD
        self.died = True
class Seeker(Enemy):
    def __init__(self, x = c.SCREEN_WIDTH, y = None, name = 'Seeker'): 
        Enemy.__init__(self)
        self.sproitsheet = setup.GFX['Asteroid']
        self.y1 = random.randint(50,450)
        self.setup_enemy(x, self.y1, name, self.setup_frames) 
        self.dmg = 2
        self.max_health = 6
        self.current_health = 6
        self.drop_money = random.randint(2,4)
        self.frame_index = 0


    def setup_frames(self):
        self.frames = []

        self.frames.append(
            self.get_image(0,0,32,32))

    def handle_state(self, powerup_group, player):
        if self.state == c.FLYING:
            self.flying()
        if self.state == c.PLAYER_DEAD:
            self.dying(powerup_group)


    def flying(self):
        if (self.current_time - self.animate_timer) > 250:
            if self.frame_index <= 0:
                self.frame_index += 1
            elif self.frame_index == 0:
                self.frame_index = 0

            self.animate_timer = self.current_time

    def dying(self,powerup_group):
        if self.current_time - self.animate_timer > 200:
            if self.frame_index <= 0:
                self.frame_index += 1
                self.animate_timer = self.current_time
            elif self.current_time - self.animate_timer > 200:
                self.kill()
                for i in range(self.drop_money):
                    powerup_group.add(powerup.Coin(self.rect.x+random.randint(0,18), self.rect.y+random.randint(0,18),10))
                if random.randint(1,100) > 95:

                    powerup_group.add(powerup.Heart(self.rect.x, self.rect.y))

    def animation(self):
        """Basic animation, switching between two frames"""
        self.image = self.frames[0]

    def transition_death(self):
            
        #gör om laserns state till prick state om den prickar något
        self.frame_index = 0
        #centerx = self.rect.centerx
        self.image = self.frames[self.frame_index]
        self.x_vel = 0
        #self.rect.centerx = centerx
        self.state = c.PLAYER_DEAD
        self.died = True

    def get_image(self, x, y, width, height):
        """Get the image frames from the sprite sheet"""
        image = pg.Surface([width, height]).convert()
        rect = image.get_rect()

        image.blit(self.sproitsheet, (0, 0), (x, y, width, height))
        image.set_colorkey(c.BLACK)


        image = pg.transform.scale(image,
                                   (int(rect.width*1),
                                    int(rect.height*1)))
        return image