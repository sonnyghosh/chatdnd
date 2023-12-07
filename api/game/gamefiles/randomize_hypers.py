import random
import sys
import os
from contextlib import redirect_stdout
CURRENT_DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.dirname(CURRENT_DIR)
sys.path.append(os.path.dirname(PARENT_DIR))
import hypers

a,b,c = hypers.load_hypers()

a = hypers.randomize(a)
b = hypers.randomize(b)

hypers.save_hypers(a,b,c)