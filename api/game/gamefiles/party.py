from . import player, g_vars
ItemType = g_vars.ItemType
PlayerStat = g_vars.PlayerStat
StatColor = g_vars.StatColor
config = g_vars.config
from game.gametests import utils
import random

class Party:
    def __init__(self, members, name):
        self.name = name
        self.players = members
    
    def validate_party(self):
        for mem in self.players:
            g = mem.validate_player()
            if not g: 
                print(f'Player: {mem.name} was invalid!')
                return False
        #print(f'{self.name} is validated {[p.name for p in self.players]}')
        return True

    def __str__(self) -> str:
        res = f'-------| {self.name} |-------\n\n'
        for pl in self.players:
            res += str(pl) + '\n\n'
        return res

    def __len__(self) -> int:
        return len(self.players)

    def get_alive_players(self):
        return [p for p in self.players if p.attr[PlayerStat.health] > 0]
    
    def get_party_members_names(self):
        res = f'{self.name}\n'
        for idx, pl in enumerate(self.get_alive_players()):
            res += f'{idx}: {pl.name} - \t'
            res += f'|{"".join([utils.colorize(f"{key.name}: {val} |", key.color().value) for key, val in pl.attr.items() if key != "name"])}'
            res += f'\t|{"".join([utils.colorize(f"{key.name}: {val} |", key.color().value) for key, val in pl.stats.items()])}\n'
        return res
    
names = ["Blaze", "Rebel", "Ace", "Rogue", "Phoenix", "Echo", "Zenith", "Valor", "Cipher", "Nova", "Trinity", "Neo", "Onyx", "Astra", "Azure", "Bex", "Briar", "Cove", "Halo", "Ivory", "Jupiter", "Kai", "Lev", "Nyx", "Reign", "Rune", "Wren", "Zephyr"]

def generate_party(n_members, squad_name, avg_level=50, level_sd=5):
    members = []
    for _ in range(n_members):
        nm = random.choice(names)
        level = int(max(0,min(100,random.normalvariate(mu=avg_level, sigma=level_sd))))
        pl = player.generate_player(nm, level)
        members.append(pl)
    return Party(members, name=squad_name)