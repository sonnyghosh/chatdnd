import random
import sys
import os
from contextlib import redirect_stdout
CURRENT_DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.dirname(CURRENT_DIR)
sys.path.append(os.path.dirname(PARENT_DIR))
from game.gamefiles import battle, party
from game.gametests import utils

num_classes = 5
master_stats = {level: {'Player':{},'Enemy':{}} for level in range(num_classes)}

num_games = 100
party_size = 3
verbose = True
for diff in range(num_games):
    level_avg = 100/(1+num_classes) * (1+ diff%num_classes)#random.randint(20,80)
    level_sd = (20/num_classes)#random.randint(1,15)
    player_party = party.generate_party(party_size, 'Dike Tyson\'s Squad', avg_level=level_avg, level_sd=level_sd)
    enemy_party = party.generate_party(party_size, 'Enemy Squad', avg_level=level_avg, level_sd=level_sd)
    current_battle = battle.Battle(player_party, enemy_party)
    if verbose:
        battle_stats = current_battle.start_game(auto_play=True)
    else:
        with redirect_stdout(open(os.devnull, 'w')):
            battle_stats = current_battle.start_game(auto_play=True)
    master_stats[diff%num_classes]['Player'] = utils.agg(master_stats[diff%num_classes]['Player'], battle_stats[0])
    master_stats[diff%num_classes]['Enemy'] = utils.agg(master_stats[diff%num_classes]['Enemy'], battle_stats[1])

print(f'Stats based on {num_games} game average.')

for level in range(num_classes):
    print('\nAVG level:', 100/(1+num_classes) * (1+ level%num_classes), '\n')
    utils.summarize('Player', master_stats[level], num_games, num_classes)
    utils.summarize('Enemy', master_stats[level], num_games, num_classes)
    utils.cross_stats(master_stats[level])

