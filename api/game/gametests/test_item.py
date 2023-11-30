import sys
import os
CURRENT_DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.dirname(CURRENT_DIR)
sys.path.append(os.path.dirname(PARENT_DIR))
import pytest
from game.gamefiles import item as item_lib

@pytest.fixture
def basic_item():
    yield item_lib.Item("Health Potion", 0, 3, {"HP": 20})

def test_item_init(basic_item):
    assert basic_item.name == "Health Potion"
    assert basic_item.cat == 0
    assert basic_item.uses == 3
    assert basic_item.effects == {"HP": 20}

def test_item_str(basic_item):
    assert str(basic_item) == "Health Potion - Type: 0 Uses: 3, Effects [ HP: 20 ]"

def test_validate_effects_valid(basic_item):
    assert basic_item.validate_effects() == True

def test_validate_effects_invalid(basic_item):
    basic_item.effects = {"HP": 150} 
    assert basic_item.validate_effects() == False

def test_use_item(basic_item):
    assert basic_item.use() == {"HP": 20}
    assert basic_item.uses == 2

def test_use_broken_item(basic_item):
    basic_item.uses = 0
    assert basic_item.use() == {}

def test_generate_items():
    bag = item_lib.generate_items(10, 100)
    assert len(bag[0]) > 0 
    assert len(bag[1]) > 0
    assert len(bag[2]) > 0
    assert len(bag[3]) > 0
    for item in bag[0]:
        assert isinstance(item, item_lib.Item)


if __name__ == "__main__":
    sys.exit(pytest.main(["-v", "-s", "./api/game/gametests/test_item.py"]))