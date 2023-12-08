import sys
import os
CURRENT_DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.dirname(CURRENT_DIR)
G_PARENT_DIR = os.path.dirname(PARENT_DIR)
sys.path.append(os.path.dirname(G_PARENT_DIR))

from backend.classes import party as party_lib
from backend.classes import player as player_lib
import pytest
from backend.game.gamefiles import g_vars as gv
ItemType = gv.ItemType
PlayerStat = gv.PlayerStat

@pytest.fixture
def basic_party():
    p1 = player_lib.generate_player("Alice", 80)
    p2 = player_lib.generate_player("Bob", 60) 
    yield party_lib.Party([p1, p2], "Test Party")

def test_party_init(basic_party):
    assert basic_party.name == "Test Party"
    assert len(basic_party.players) == 2

def test_validate_party_valid(basic_party):
    assert basic_party.validate_party() == True

def test_validate_party_invalid(basic_party):
    basic_party.players[0].attr[PlayerStat.level] = -10  
    assert basic_party.validate_party() == False

def test_get_alive_players(basic_party):
    alive = basic_party.get_alive_players()
    assert len(alive) == len(basic_party.players)

def test_get_party_members_names(basic_party):
    names = basic_party.get_party_members_names()
    assert "Alice" in names 
    assert "Bob" in names

def test_generate_party():
    party = party_lib.generate_party(5, "New Party")
    assert isinstance(party, party_lib.Party)
    assert len(party.players) == 5
    assert party.name == "New Party"

if __name__ == "__main__":
    sys.exit(pytest.main(["-v", "-s", "./api/game/gametests/test_party.py"]))