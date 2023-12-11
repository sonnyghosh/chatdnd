import random
import sys
import os
CURRENT_DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.dirname(CURRENT_DIR)
G_PARENT_DIR = os.path.dirname(PARENT_DIR)
sys.path.append(os.path.dirname(G_PARENT_DIR))

from backend.classes import battle, party
from backend.game.gametests import utils

player_party = party.generate_party(4, 'Dike Tyson\'s Squad', avg_level=52)
print(player_party.get_inputs())
print('Your Power level: ',player_party.get_power_level())
enemy_party = party.generate_party(5, 'Enemy Squad', avg_level=50)
print('Enemy Power level: ',enemy_party.get_power_level())
current_battle = battle.Battle(player_party, enemy_party)
game_stats = current_battle.start_game()
utils.summarize('Player', game_stats)
utils.summarize('Enemy', game_stats)
utils.cross_stats(game_stats)