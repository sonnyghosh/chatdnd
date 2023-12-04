import random
import sys
import os
import math
from contextlib import redirect_stdout
CURRENT_DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.dirname(CURRENT_DIR)
sys.path.append(os.path.dirname(PARENT_DIR))
import hypers
from game.gametests.auto_test_game import test_game

item_hypers, player_hypers, meta_params = hypers.load_hypers() 

num_tests = 1000

correct_preds = 0
for lev in range(num_tests):
    if random.random() > 0.99:
        party_size = random.randint(1,6)
        _, ratio, win = test_game(party_size=party_size, level=(lev%10+1)*10, generate_party=True)
    else:
        party_size = random.randint(1,5)
        cur_lev = (lev%9+2)*10
        _, ratio, win = test_game(party_size=(party_size, party_size+1), level=(cur_lev, cur_lev-10), generate_party=True)

    correct_preds += 1 if ratio >= 1 and win == 1 else 1 if ratio <= 1 and win == 0 else 0

print(num_tests, correct_preds)


