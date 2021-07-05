#! python3
import sys
import os
import pygame
from pygame.locals import *

from scripts.player import Player
from scripts.obstacle import Obstacle
from scripts.projectile import Projectile
from scripts.text import Text
from scripts.Explorer import *
from scripts.Heart import Heart
from scripts.attackBoost import atkBoost
import random
class Level():


    def __init__(self):
        self.X = 5
        pygame.init()


        self.width, self.height = 1100, 500
        self.win = pygame.display.set_mode((self.width, self.height))
        #pygame.display.set_caption('Space Blaster')

        self.bg = pygame.image.load(os.path.join('assets', 'sprites', 'background.png'))
        self.bgX = 0
        self.bgX2 = self.bg.get_width()

        self.clock = pygame.time.Clock()

        self.player = Player(3, 200, 200)



        self.pressed = {}
        self.run = True
        self.asteroider = list()
        self.enemies = list()
        self.projektiler = list()
        self.items = list()
        self.a = Obstacle()
        self.timeSinceLastAsteroidSpawn = 0
        self.timeSinceLastEnemySpawn = 0
        self.timeSinceLastItemSpawn = 0
        self.bossTimer = 0

  
        

        
            

    def redrawWindow(self):
        self.win.blit(self.bg, (self.bgX, 0))
        self.win.blit(self.bg, (self.bgX2, 0))
        self.player.draw(self.win)


        if self.player.dash != True:
            self.tempX = self.player.X
            self.tempY = self.player.Y
        if self.player.dash:
            self.win.blit(self.player.dashImg, (self.tempX, self.tempY))
            self.player.drawDash(self.win)
            if self.player.timeSinceLastDash > 800:
                self.player.dash = False
                self.player.timeSinceLastDash = 0

    

        for obj in self.asteroider:
            obj.draw(self.win)
            obj.moove(5)
            if obj.X < -30:
                self.asteroider.remove(obj)
                break
     
            if obj.get_rect().colliderect(self.player.get_rect()):
                self.asteroider.remove(obj)
                self.player.damageTaken(1)
                break
            for ob in self.player.projektiler:
                if ob.get_rect().colliderect(obj.get_rect()):
                    try:
                        self.asteroider.remove(obj)
                    except:
                        print("error")
                    self.player.projektiler.remove(ob)
                    self.player.Score += 100
                    print(self.player.Score)

            
        for obj in self.player.projektiler:
            obj.draw(self.win)

            if obj.X > 1200:
                self.player.projektiler.remove(obj)
            for i in self.enemies:
                if i.get_rect().colliderect(obj.get_rect()):
                    i.Health -= self.player.dmg
                    if i.Health < 0:
                        self.enemies.remove(i)
                        self.player.Score += i.giveScore

                        if i.giveScore == ExplorerBoss().giveScore:
                            print("YOU WIN!")

        for obj in self.player.enemyProjektiler:
            obj.draw(self.win)

            if obj.X < -30:
                self.player.enemyProjektiler.remove(obj)

            if self.player.get_rect().colliderect(obj.get_rect()):
                print("AJJJ")
                self.player.damageTaken(1)
                self.player.enemyProjektiler.remove(obj)

    

        for obj in self.enemies:
            obj.draw(self.win)

            if obj.X < -30:
                self.enemies.remove(obj)

        for obj in self.items:
            obj.draw(self.win)

            if obj.X < -30:
                self.items.remove(obj)

            if self.player.get_rect().colliderect(obj.get_rect()):
                if hasattr(obj, 'Healing'):
                    self.player.Health += obj.Healing
                if hasattr(obj, 'AttackBoost'):
                    self.player.dmg += obj.AttackBoost
                self.items.remove(obj)
                print("You just got healed boi")

        pygame.display.update()
        

    def draw(self):
        rand = random.randint(0,100)
        self.redrawWindow()
        self.bgX -= 1.4
        self.bgX2 -= 1.4

        #Spawning asteroids
        self.dt = self.clock.tick()
        self.timeSinceLastAsteroidSpawn += self.dt
        if self.timeSinceLastAsteroidSpawn > 300:
            self.timeSinceLastAsteroidSpawn = 0
            self.asteroider.append(Obstacle())
    
        #Spawning enemies
        self.timeSinceLastEnemySpawn += self.dt
        if self.timeSinceLastEnemySpawn > 1200:
            self.timeSinceLastEnemySpawn = 0
            self.enemies.append(Explorer())

        #Spawning items
        self.timeSinceLastItemSpawn += self.dt
        if self.timeSinceLastItemSpawn > 10000:
            self.timeSinceLastItemSpawn = 0
            if rand > 51:

                self.items.append(Heart(1))
            elif rand < 49:
                self.items.append(atkBoost(1))

        self.bossTimer += self.dt
        if self.bossTimer > 30000 and self.bossTimer < 200000:
            self.bossTimer = 210000
            self.enemies.append(ExplorerBoss())

        self.player.timeSinceLastDash += self.dt
        


        #Shoot weapon
        self.player.shoot(self.dt)

        for i in self.enemies:
            i.shoot(self.dt, self.player)


        #Background scrolling
        if self.bgX < self.bg.get_width() * -1:
            self.bgX = self.bg.get_width()
        if self.bgX2 < self.bg.get_width() * -1:
            self.bgX2 = self.bg.get_width()


        #Controls
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                
                pygame.quit()


            #Movement
            if event.type == pygame.KEYDOWN:

                #Movement controls
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    self.player.control(-self.player.Speed,0)
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    self.player.control(self.player.Speed,0)

                if event.key == pygame.K_UP or event.key == ord('w'):
                    self.player.control(0,-self.player.Speed)
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    self.player.control(0, self.player.Speed)

                if event.key == pygame.K_p:
                    run = False


                #Skill controls
                if event.key == pygame.K_SPACE:
                    if self.player.timeSinceLastSkill > 2500:
                        self.player.skillShot()

                if event.key == pygame.K_LSHIFT:
                    if self.player.dash == False:
                        self.player.skillDash(self.win)
                        self.player.dash = True
                    
            
            if event.type == pygame.KEYUP:
                #Movement controls
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    self.player.control(self.player.Speed,0)
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    self.player.control(-self.player.Speed,0)
                if event.key == pygame.K_UP or event.key == ord('w'):
                    self.player.control(0, self.player.Speed)
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    self.player.control(0, -self.player.Speed)