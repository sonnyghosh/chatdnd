from game import item

class Character:
    def __init__(self, stats, attr,**items) -> None:
        self.ATK = stats['ATK']
        self.DEF = stats['DEF']
        self.CHA = stats['CHA']
        self.INT = stats['INT']
        self.WIS = stats['WIS']
        self.lvl = attr['level']
        self.HP = attr['health']
        self.MP = attr['mana']
        self.STA = attr['stamina']
        self.name = attr['name']
        self.items = items
    