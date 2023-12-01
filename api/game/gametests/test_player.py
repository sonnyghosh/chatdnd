import sys
import os
import random
CURRENT_DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.dirname(CURRENT_DIR)
sys.path.append(os.path.dirname(PARENT_DIR))
import pytest
from game.gamefiles import player as player_lib
from game.gamefiles import item as item_lib
from game.gamefiles import g_vars as gv
ItemType = gv.ItemType
PlayerStat = gv.PlayerStat

@pytest.fixture 
def basic_player():
    yield player_lib.generate_player("Bob")

def test_player_init(basic_player):
    assert isinstance(basic_player.name, str)
    assert len(basic_player.stats) == 5
    assert 0 <= basic_player.stats[PlayerStat.attack] <= 50
    assert len(basic_player.attr) == 5
    assert 0 <= basic_player.attr[PlayerStat.level] <= 100

def test_validate_player_valid(basic_player):  
    assert basic_player.validate_player() == True

def test_validate_player_invalid(basic_player):
    basic_player.attr[PlayerStat.health] = -10
    assert basic_player.validate_player() == False

def test_get_melee(basic_player):
    weapons = basic_player.get_item_type(ItemType.melee)
    assert isinstance(weapons, list)
    assert all(isinstance(w, item_lib.Item) for w in weapons)

def test_get_ranged(basic_player):
    weapons = basic_player.get_item_type(ItemType.ranged)
    assert isinstance(weapons, list)
    assert all(isinstance(w, item_lib.Item) for w in weapons)

def test_use_item(basic_player):
    item = item_lib.Item(ItemType.potion, 1, {PlayerStat.health: 10})
    basic_player.attr[PlayerStat.health] = 90
    basic_player.use(item)
    assert basic_player.attr[PlayerStat.health] == 100

def test_attack(basic_player):
    enemy = player_lib.generate_player("Enemy")
    basic_player.attack(enemy)
    assert enemy.attr[PlayerStat.health] < 100  

def test_generate_player():
    player = player_lib.generate_player("Test")
    assert 0 <= player.attr[PlayerStat.level] <= 100
    assert len(player.items) == 5

def test_give_item(basic_player):
    player = player_lib.generate_player("Test")
    item_ind = random.choice(list(ItemType))
    item_choice = random.choice(basic_player.items[item_ind])
    basic_player.give(item_choice, player)
    assert not item_choice in basic_player.items[item_ind]
    assert item_choice in player.items[item_ind]

if __name__ == "__main__":
    sys.exit(pytest.main(["-v", "-s", "./api/game/gametests/test_player.py"]))