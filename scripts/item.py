
class Item(object):
    def __init__(self, id, name , stack, type, value, rarity):
        super(Item, self).__init__()
        self.id = id
        self.stack = stack
        self.name = name
        self.value = value
        self.rarity = rarity

        #1: equip 2:misc 3:pet
        self.type = type

    def set_position(position):
        super(self, position).set_position()
        self.position = position

class Weapon(object):
    def __init__(self,id,name,stack,type,value,rarity,damage):
        self.id = id
        self.stack = stack
        self.name = name
        self.value = value
        self.rarity = rarity
        self.damage = damage

        #1: equip 2:misc 3:pet
        self.type = type

class Armor(object):
    def __init__(self,id,name,stack,type,value,rarity,hp):
        self.id = id
        self.stack = stack
        self.name = name
        self.value = value
        self.rarity = rarity
        self.hp = hp

        #1: equip 2:misc 3:pet
        self.type = type




