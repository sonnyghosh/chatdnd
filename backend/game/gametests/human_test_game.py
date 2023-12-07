import random
import sys
import os
CURRENT_DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.dirname(CURRENT_DIR)
sys.path.append(os.path.dirname(PARENT_DIR))
from game.gamefiles import battle, party
from game.gametests import utils

player_party = party.generate_party(2, 'Dike Tyson\'s Squad', avg_level=100)
print(player_party.get_inputs())
print('Your Power level: ',player_party.get_power_level())
enemy_party = party.generate_party(3, 'Enemy Squad', avg_level=80)
print('Enemy Power level: ',enemy_party.get_power_level())
current_battle = battle.Battle(player_party, enemy_party)
game_stats = current_battle.start_game()
utils.summarize('Player', game_stats)
utils.summarize('Enemy', game_stats)
utils.cross_stats(game_stats)