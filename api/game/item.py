

class item:

    def __init__(self, attrs) -> None:
        self.breakable = attrs['break']
        self.uses = -1 if not self.breakable else attrs['uses']
        self.broken = True if self.uses == 0 else False
        self.effects = attrs['effects'] # {'ATK': 5, 'DEF': 2} - increase attack by 5 and defense by 2

    def use(self) -> int:
        if not self.broken:
            for stat in self.effects:
                pass
            if self.breakable:
                self.uses -= 1
            return 0
        else:
            return -1