from game import item

'''
stats = {
    'ATK': 0-50,
    'DEF': 0-50,
    'CHA': 0-50,
    'INT': 0-50,
    'WIS': 0-50
}

attr = {
    'level': 0-100,
    'health': 0-100,
    'stamina': 0-100,
    'name': str,
}

items = [Item()...]
'''

class Player:
    def __init__(self, stats, attr, items):
        self.name = attr['name']
        self.stats = stats
        self.attr = attr
        self.items = items
    
    def __str__(self) -> str:
        # print out the name of the player
        res = f'\t--------| {self.name} |---------\n'

        # print all of the player stats
        res += '\tStats:'
        for st, val in self.stats.items():
            res += f'\n\t\t{st} - {val}'

        # print out the attributes of th player
        res += '\n\tAttributes:'
        for st, val in self.attr.items():
            res += f'\n\t\t{st} - {val}'

        #print out player items
        res += '\n\tItems:'
        for it in self.items:
            res += f'\n\t\t{it}'

        res += '\n\t-------------------------'
        return res

    def attack(self, target):
        damage = self.stats["ATK"] - target.stats["DEF"]
        target.attr["HP"] -= damage
        
    def use_item(self, item, target):
        item.use(self, target)
        self.attr["STA"] -= 10

