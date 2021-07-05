
from scripts import item
import xlrd
import os
import pygame
from scripts.data import tools
from scripts.data import constant as c

ORIGINAL_CAPTION = c.ORIGINAL_CAPTION

pygame.init()
pygame.event.set_allowed([pygame.KEYDOWN, pygame.KEYUP, pygame.QUIT])
pygame.display.set_caption(c.ORIGINAL_CAPTION)
Screen = pygame.display.set_mode(c.SCREEN_SIZE)

myfont = pygame.font.SysFont("arialblack", 11)
myfont_money = pygame.font.SysFont("monospace", 30)
myfont_itemtitle = pygame.font.SysFont("arialblack", 15)



GFX = tools.load_all_gfx(os.path.join("assets", "sprites"))
SFX = tools.load_all_sfx(os.path.join("assets", "sounds"))

wb = xlrd.open_workbook(os.path.join("assets", "Database", "items.xlsx")) 
sheet = wb.sheet_by_index(0)

wb_weapon = xlrd.open_workbook(os.path.join("assets", "Database", "weapons.xlsx"))
sheet_wep = wb_weapon.sheet_by_index(0)

wb_armors = xlrd.open_workbook(os.path.join("assets", "Database", "armors.xlsx"))
sheet_arm = wb_armors.sheet_by_index(0)

items = [1]
items_pictures = [1]

weapons = [1]
weapons_pictures = [1]

armors = [1]
armors_pictures = [1]

for i in range(1, sheet.nrows):
    item_values = []
    for j in range(sheet.ncols):
        item_values.append(sheet.cell_value(i,j))
    items.append(item.Item(int(item_values[0]),item_values[1],item_values[2],item_values[3],int(item_values[4]), item_values[5]))

for i in range(1, sheet_wep.nrows):
    weapon_values = []
    for j in range (sheet_wep.ncols):
        weapon_values.append(sheet_wep.cell_value(i,j))
    weapons.append(item.Weapon(int(weapon_values[0]),weapon_values[1],weapon_values[2],weapon_values[3],int(weapon_values[4]), weapon_values[5], int(weapon_values[6])))

for i in range(1, sheet_arm.nrows):
    weapon_values = []
    for j in range (sheet_arm.ncols):
        weapon_values.append(sheet_arm.cell_value(i,j))
    armors.append(item.Armor(int(weapon_values[0]),weapon_values[1],weapon_values[2],weapon_values[3],int(weapon_values[4]), weapon_values[5], int(weapon_values[6])))




items_pictures.append(GFX['Gem_17'])
items_pictures.append(GFX['Gem_17'])
items_pictures.append(GFX['Gem_17'])
items_pictures.append(GFX['Gem_17'])
items_pictures.append(GFX['Gem_17'])

weapons_pictures.append(GFX['Rifle_24']) #Starter weapon Laser cannon
weapons_pictures.append(GFX['Rifle_24'])
weapons_pictures.append(GFX['Rifle_24'])
weapons_pictures.append(GFX['106_1'])#pretty good weapons boi
weapons_pictures.append(GFX['Rifle_26'])

armors_pictures.append(GFX['Plate20'])



