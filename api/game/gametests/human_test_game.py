import random
import sys
import os
CURRENT_DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.dirname(CURRENT_DIR)
sys.path.append(os.path.dirname(PARENT_DIR))
from game.gamefiles import battle, party
from game.gametests import utils

player_party = party.generate_party(1, 'Dike Tyson\'s Squad', avg_level=100)
print(player_party)
enemy_party = party.generate_party(1, 'Enemy Squad', avg_level=20)
print(enemy_party)
current_battle = battle.Battle(player_party, enemy_party)
game_stats = current_battle.start_game()
utils.summarize('Player', game_stats)
utils.summarize('Enemy', game_stats)
utils.cross_stats()