import random
import sys
import os
CURRENT_DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.dirname(CURRENT_DIR)
sys.path.append(os.path.dirname(PARENT_DIR))
from game.gamefiles import battle, party

def agg(store, sample):
    store.update({key: store.get(key, 0) + val for key, val in sample.items()})
    return store

def colorize(text, color):
    colors = {
        'reset': '\033[0m',
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'purple': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m'
    }
    return f'{colors[color]}{text}{colors["reset"]}'

def summarize(title, dicti):
    A = ["ATK","ATK","STA","STA","MP","MP","HP","HP"]
    B = ["turns","moves","turns","moves","turns","moves","turns","moves"]
    print(colorize(f'{title}:', 'blue'))
    for key, val in dicti[title].items():
        print(f'\t {colorize(f"avg {key}", "white")} - {colorize(f"Total:{val} - Avg:{val/num_games}", "red" if val < 0 else "green")}')
    for a, b in zip(A,B):
        val = dicti[title][a]/dicti[title][b]
        print(f'{colorize(f"{a}/{b}", "white")} : {colorize(round(val, ndigits=2), "red" if val < 0 else "green")}')

master_stats = {
    'Player':{},
    'Enemy':{} 
}

num_games = 10
party_size = 3
for _ in range(num_games):
    level_avg = 10#random.randint(20,80)
    level_sd = 2#random.randint(1,15)
    player_party = party.generate_party(party_size, 'Dike Tyson\'s Squad', avg_level=level_avg, level_sd=level_sd)
    enemy_party = party.generate_party(party_size, 'Enemy Squad', avg_level=level_avg, level_sd=level_sd)
    current_battle = battle.Battle(player_party, enemy_party)
    battle_stats = current_battle.start_auto()
    master_stats['Player'] = agg(master_stats['Player'], battle_stats[0])
    master_stats['Enemy'] = agg(master_stats['Enemy'], battle_stats[1])

print(f'Stats based on {num_games} game average.')

summarize('Player', master_stats)
summarize('Enemy', master_stats)

