from enum import Enum

class ItemType(Enum):
    potion = 0
    magic = 1
    weapon = 2
    armor = 3

class PlayerStat(Enum):  
    attack = 'ATK'
    defense = 'DEF' 
    charisma = 'CHA'
    intelligence = 'INT'
    wisdom = 'WIS'
    health = 'HP'
    mana = 'MP'
    stamina = 'STA'  
    level = 'LVL'
    
    def color(self):
        color_map = {
            PlayerStat.attack: StatColor.attack,
            PlayerStat.defense: StatColor.defense,
            PlayerStat.charisma: StatColor.charisma, 
            PlayerStat.intelligence: StatColor.intelligence,
            PlayerStat.wisdom: StatColor.wisdom,
            PlayerStat.health: StatColor.health,
            PlayerStat.mana: StatColor.mana,
            PlayerStat.stamina: StatColor.stamina,
            PlayerStat.level: StatColor.level
        }
        return color_map.get(self)

class StatColor(Enum):
    attack = ['bold', 'bright_red', 'on_black']
    defense = ['bold', 'bright_green', 'on_black']
    charisma = ['bold','bright_blue', 'on_white']
    intelligence = ['bold','bright_green', 'on_white']
    wisdom = ['bold','bright_magenta', 'on_white']
    health = ['bold','green', 'on_black']
    mana = ['bold','magenta', 'on_bright_black']
    stamina = ['bold','bright_yellow', 'on_bright_black']
    level = ['bold','white', 'on_black']

stats = [PlayerStat.attack, PlayerStat.defense, PlayerStat.charisma, PlayerStat.intelligence, 
         PlayerStat.wisdom, PlayerStat.health, PlayerStat.mana, PlayerStat.stamina, PlayerStat.level]

choices = {
    ItemType.potion: stats[:-1],
    ItemType.magic: stats[:-4],
    ItemType.weapon: stats[0],
    ItemType.armor: stats[1]
}

config = {
    "meta": {

    },
    "item": {
        "names": ["potion", "magic", "weapon", "armor"]
    },
    "weapon": {

    },
    "magic": {

    },
    "player": {
        "avg_level": 50,
        "avg_sd": 10
    }
}

