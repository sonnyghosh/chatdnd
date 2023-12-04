import sys
import os
CURRENT_DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.dirname(CURRENT_DIR)
sys.path.append(os.path.dirname(PARENT_DIR))
import pytest
from game.gamefiles import item as item_lib
from game.gamefiles import g_vars as gv
ItemType = gv.ItemType
PlayerStat = gv.PlayerStat

@pytest.fixture
def basic_item():
    yield item_lib.Item(ItemType.potion, 3, {PlayerStat.health: 20})

def test_item_init(basic_item):
    assert basic_item.type == ItemType.potion
    assert basic_item.uses == 3
    assert basic_item.effects == {PlayerStat.health: 20}

def test_item_str(basic_item):
    assert str(basic_item) == "potion - Rank: 6, Uses: 3, Effects [ HP: 20 ]"

def test_validate_effects_valid(basic_item):
    assert basic_item.validate_effects() == True

def test_validate_effects_invalid(basic_item):
    basic_item.effects = {PlayerStat.health: 150} 
    assert basic_item.validate_effects() == False

def test_use_item(basic_item):
    assert basic_item.use() == {PlayerStat.health: 20}
    assert basic_item.uses == 2

def test_use_broken_item(basic_item):
    basic_item.uses = 0
    assert basic_item.use() == {}

def test_generate_items():
    bag = item_lib.generate_items(10, 100)
    assert len(bag[ItemType.potion]) > 0 
    assert len(bag[ItemType.magic]) > 0
    assert len(bag[ItemType.ranged]) > 0
    assert len(bag[ItemType.melee]) > 0
    assert len(bag[ItemType.armor]) > 0
    for item_list in bag.values():
        for item in item_list:
            assert isinstance(item, item_lib.Item)


if __name__ == "__main__":
    sys.exit(pytest.main(["-v", "-s", "./api/game/gametests/test_item.py"]))