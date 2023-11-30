from enum import Enum

class ItemType(Enum):
    potion = 0
    magic = 1
    weapon = 2
    armor = 3

class PlayerStat(Enum):
    attack =' ATK'
    defense = 'DEF'
    charisma = 'CHA'
    intelligence = 'INT'
    wisdom = 'WIS'
    health = 'HP'
    mana = 'MP'
    stamina = 'STA'
    level = 'LVL'

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

