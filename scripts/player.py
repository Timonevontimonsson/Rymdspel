#! python3
from scripts.creature import Creature
from scripts.projectile import Projectile
import pygame as pg
import os
from scripts.data import setup, tools
from scripts.data import constant as c
from scripts import powerup
from scripts import inventory
from scripts import ammo
from scripts import shield

class Player(pg.sprite.Sprite):


    def __init__(self, save = None):
        pg.sprite.Sprite.__init__(self)
        self.sprite_sheet = setup.GFX['spaceshipcool']
        self.setup_timers()
        self.setup_state_booleans()
        self.setup_forces()
        self.setup_counters()
        self.load_images_from_sheet()
        self.ship = 'phoenix'

        self.health = 82
        self.max_health = 82
        self.current_shield = 10
        self.maximum_shield = 10
        self.shield_active = False
        self.base_dmg = 1
        self.dmg = 1
        self.rocket_dmg = 10
        self.shotgun_dmg = 5
        self.base_shotgun_dmg = 5
        self.base_rocket_dmg = 10
        self.speed = 6
        
        
        self.ammo_t1 = ammo.Ammo('Tier 1 ammo', 1, 1, 0)
        self.ammo_t2 = ammo.Ammo('Tier 2 ammo',2, 25, 0)
        self.ammo_tier_GOD = ammo.Ammo('Tier GOD ammo', 50, 9999999, 99999)

        self.ammo = ammo.Ammo('Tier 1 ammo', 1, 1, 5)
        self.credits = 10
        self.weapon = "Dual Blaster"
        self.shield_regen_timer = 1000
        

        self.state = c.IDLE
        self.image = self.ship_frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)

        self.key_timer = 0

        self.powerup_group = []

        self.projektiler = []
        self.enemyProjektiler = []
        
        self.player_inventory = inventory.Inventory(32)
        self.equipment = inventory.Equipment(self.ship)


        self.inventory = {#vapen
                                  'Blaster':1,
                                  'Dual Blaster':1,
                                  #ammo
                                  self.ammo_t1.name: 50,
                                  self.ammo_t2.name: 60,
                                  #currency
                                  'gold':0
            }
        self.shield = shield.Shield(40, -32, self.maximum_shield)


    def setup_timers(self):
        self.accelerate_timer = 0
        self.fire_timer = 0
        self.animate_timer = 0
        self.dash_timer = 0
        self.hurt_timer = 0
        self.death_timer = 0
        self.shoot_timer = 0
        self.last_fire_timer = 0
        self.current_time = 0
        self.rocket_timer = 0
        self.shield_cooldown_timer = 0
        self.flash_counter = 0
        self.shotgun_timer = 0

    def setup_state_booleans(self):
        self.accelerate = False
        self.allow_fire = True
        self.allow_dash = True
        self.dead = False
        self.allow_shotgun_fire = False

    def setup_forces(self):
        self.x_vel = 0
        self.y_vel = 0
        self.x_accel = c.X_ACCEL
        self.y_accel = c.Y_ACCEL


    def setup_counters(self):
        self.frame_index = 0
        self.fire_transition_index = 0
        self.fire_count = 0

    def load_images_from_sheet(self):
        self.ship_frames = []

        for i in range(8):
            self.ship_frames.append(self.get_image(i*81,0, 81, 38))


    def get_image(self, x, y, width, height):
        """Extracts image from sprite sheet"""
        image = pg.Surface([width, height])
        rect = image.get_rect()

        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(c.BLACK)
        image = pg.transform.scale(image,
                                   (int(rect.width*0.7),
                                    int(rect.height*0.7)))
        return image

    def update(self, keys, game_info, group):
        """Updates Mario's states and animations once per frame"""
        self.current_time = pg.time.get_ticks()
        self.handle_state(keys, group)
        self.animation()
        self.update_inventory()
        self.regen()
    def regen(self):
        if self.shield_regen_timer == 1000:
            self.shield_regen_timer += self.current_time
        elif self.current_time - self.shield_regen_timer > 0:
            if self.current_shield < self.maximum_shield:
                self.current_shield += 1
                self.shield_regen_timer = 1000
                print(self.current_shield)

    def update_inventory(self):
        self.ammo_t1.amount = self.inventory[self.ammo_t1.name]
        self.ammo_t2.amount = self.inventory[self.ammo_t2.name]

    
    def handle_state(self, keys, group):
        #Bestämmer spelarens beteende baserat på hans status
        if self.state == c.IDLE:
            self.idling(keys, group)
        elif self.state == c.FLYING:
            self.flying(keys, group)
        self.animation()


    def idling(self, keys, group):
        "Om spelaren inte rör sig"
        
        self.x_acc = 0
        self.y_acc = 0

        if keys[tools.keybinding['down']] or keys[tools.keybinding['up']] or keys[tools.keybinding['left']] or keys[tools.keybinding['right']]:
            self.state = c.FLYING
        else:
            self.state = c.IDLE

          
        self.check_to_allow_laser(group)

    def flying(self, keys, group):
        
        
            
        self.check_to_allow_laser(group)

        

        
    def check_to_allow_laser(self, group):
        """Check to allow the shooting of a laser"""
        if self.shoot_timer == 0:
            
            self.shoot_timer = self.current_time
        elif self.current_time - self.shoot_timer > 500:
            self.shoot_laser(group)
            self.shoot_timer = self.current_time
        if self.shotgun_timer == 0:
            self.shotgun_timer = self.current_time
        elif self.current_time - self.shotgun_timer > 400:
            self.allow_shotgun_fire = True
            self.shotgun_timer = 0

    def create_shield(self, shield_group):
            if self.current_time - self.shield_cooldown_timer > 0:
                shield_group.add(self.shield)
                self.shield_active = True
                self.shield_cooldown_timer = 5000
            if self.shield_cooldown_timer == 5000:
                self.shield_cooldown_timer += self.current_time
                
        

    def shoot_laser(self,powerup_group):
        #setup.SFX['laser_sound_effect'].play()

        
        self.dmg = self.base_dmg * self.ammo.atk


        if self.ammo.amount > 0:
            if self.weapon == 'Blaster':
                powerup_group.add(powerup.Laser(self.rect.right+5, self.rect.y,self.dmg))
                self.inventory[self.ammo.name] -= 1
            elif self.weapon == 'Dual Blaster':
                powerup_group.add(powerup.Laser(self.rect.right+5, self.rect.y,self.dmg))
                powerup_group.add(powerup.Laser(self.rect.right+5, self.rect.y- 15,self.dmg))
                self.inventory[self.ammo.name] -= 2
            elif self.weapon == 'Shotgun' and self.allow_shotgun_fire and False:
                powerup_group.add(powerup.Laser(self.rect.right + 5, self.rect.y,'Shotgun',7,0))
                powerup_group.add(powerup.Laser(self.rect.right + 5, self.rect.y+5,'Shotgun',7,1))
                powerup_group.add(powerup.Laser(self.rect.right + 5, self.rect.y+10,'Shotgun',7,2))
                powerup_group.add(powerup.Laser(self.rect.right + 5, self.rect.y+15, 'Shotgun',7,3))
                powerup_group.add(powerup.Laser(self.rect.right + 5, self.rect.y-5, 'Shotgun',7,-1))
                powerup_group.add(powerup.Laser(self.rect.right + 5, self.rect.y-10, 'Shotgun',7,-2))
                powerup_group.add(powerup.Laser(self.rect.right + 5, self.rect.y-15, 'Shotgun', 7, -3))
                self.allow_shotgun_fire = False



    def shoot_rockets(self, powerup_group):
        if self.current_time - self.rocket_timer > 50:
            powerup_group.add(powerup.Laser(self.rect.right+5, self.rect.y, 'rocket'))
            #powerup_group.add(powerup.Laser(self.rect.right+5, self.rect.y+5, 'rocket'))
            #powerup_group.add(powerup.Laser(self.rect.right+5, self.rect.y+10, 'rocket'))
            #powerup_group.add(powerup.Laser(self.rect.right+5, self.rect.y-5, 'rocket'))
            #powerup_group.add(powerup.Laser(self.rect.right+5, self.rect.y-10, 'rocket'))
            self.rocket_timer = 0
        if self.rocket_timer == 0:
            self.rocket_timer = self.current_time
        
    def animation(self):
        
        if self.current_time - self.animate_timer > 50:
            if self.frame_index <= 6:
                self.frame_index += 1
            elif self.frame_index == 7:
                self.frame_index = 3
                self.flash_counter += 1
            self.animate_timer = self.current_time
        if self.flash_counter == 5:
            self.frame_index = 0
            self.flash_counter = 0


        self.image = self.ship_frames[self.frame_index]






   



