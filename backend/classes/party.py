from . import player, class_utils
from backend.game.gamefiles import g_vars
ItemType = g_vars.ItemType
PlayerStat = g_vars.PlayerStat
StatColor = g_vars.StatColor
config = g_vars.config
from game.gametests import utils
import random
db = class_utils.db

def average_arrays(lists):
    result = []
    for i in range(len(lists[0])):
        values = [list[i] for list in lists]
        avg = sum(values) / len(values)
        result.append(avg)
    return result

class Party:
    def __init__(self, members, name):
        self.name = name
        self.players = members
        self.id = class_utils.generate_id()
    
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
        res = [p for p in self.players if p.attr[PlayerStat.health] > 0]
        res.sort(key=lambda x: x.get_rank())
        return res
    
    def get_power_level(self):
        cur_pt = self.get_alive_players()
        return max(0.01,sum([pl.get_rank() for pl in cur_pt]))

    def get_unputs(self):
        pass

    def get_party_members_names(self):
        res = f'{self.name}\n'
        for idx, pl in enumerate(self.get_alive_players()):
            res += f'{idx}: {pl.name} - {pl.get_rank()}\t'
            res += f'|{"".join([utils.colorize(f"{key.name}: {val} |", key.color().value) for key, val in pl.attr.items() if key != "name"])}'
            res += f'\t|{"".join([utils.colorize(f"{key.name}: {val} |", key.color().value) for key, val in pl.stats.items()])}\n'
        return res
    
    def get_inputs(self):
        arrs = [pl.get_inputs() for pl in self.get_alive_players()]
        return average_arrays(arrs) + [self.get_power_level()] 
    
    def asdict(self):
        return {'name': self.name, 'players': self.players, 'id': self.id}

    # TODO: add in a buy item and assign item function

names = ["Blaze", "Rebel", "Ace", "Rogue", "Phoenix", "Echo", "Zenith", "Valor", "Cipher", "Nova", "Trinity", "Neo", "Onyx", "Astra", "Azure", "Bex", "Briar", "Cove", "Halo", "Ivory", "Jupiter", "Kai", "Lev", "Nyx", "Reign", "Rune", "Wren", "Zephyr"]

def generate_party(n_members, squad_name, avg_level=50, level_sd=5):
    members = []
    nm = random.choices(names, k=n_members)
    for i in range(n_members):
        level = int(max(0,min(100,random.normalvariate(mu=avg_level, sigma=level_sd))))
        pl = player.generate_player(nm[i], level)
        members.append(pl)
    return Party(members, name=squad_name)