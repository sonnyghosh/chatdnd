import random
import sys
import os
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
    _, ratio, win = test_game(party_size=5, level=(lev%10+1)*10, generate_party=True)
    correct_preds += 1 if ratio >= 1 and win == 1 else 1 if ratio <= 1 and win == 0 else 0
fit = correct_preds/num_tests

print(fit)


