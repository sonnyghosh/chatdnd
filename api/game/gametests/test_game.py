import random
import sys
import os
CURRENT_DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.dirname(CURRENT_DIR)
sys.path.append(os.path.dirname(PARENT_DIR))
from gamefiles import battle, party

player_party = party.generate_party(3, 'Dike Tyson\'s Squad')
print(player_party)
enemy_party = party.generate_party(3, 'Enemy Squad')
print(enemy_party)
current_battle = battle.Battle(player_party, enemy_party)
current_battle.start()