import sys
import os
CURRENT_DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.dirname(CURRENT_DIR)
G_PARENT_DIR = os.path.dirname(PARENT_DIR)
sys.path.append(os.path.dirname(G_PARENT_DIR))


