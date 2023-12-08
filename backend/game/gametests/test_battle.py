import sys
import os
CURRENT_DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.dirname(CURRENT_DIR)
G_PARENT_DIR = os.path.dirname(PARENT_DIR)
sys.path.append(os.path.dirname(G_PARENT_DIR))

from backend.classes import battle as battle_lib
from backend.classes import party as party_lib
from backend.classes import player as player_lib
import pytest
from backend.game.gamefiles import g_vars as gv
ItemType = gv.ItemType
PlayerStat = gv.PlayerStat

@pytest.fixture
def basic_battle():
    p1 = player_lib.generate_player("Alice", level=100)
    p2 = player_lib.generate_player("Bob", level=100)
    player_party = party_lib.Party([p1, p2], "Heroes")
    
    e1 = player_lib.generate_player("Zog", level=10) 
    e2 = player_lib.generate_player("Vog", level=10)
    enemy_party = party_lib.Party([e1, e2], "Enemies")
    
    yield battle_lib.Battle(player_party, enemy_party)

def test_battle_init(basic_battle):
    assert isinstance(basic_battle.player_party, party_lib.Party)
    assert isinstance(basic_battle.enemy_party, party_lib.Party)   

def test_agg():
    store = {}
    sample = {PlayerStat.health: 10, PlayerStat.mana: 5}
    updated = battle_lib.agg(store, sample)
    assert updated == sample

def test_player_turn(basic_battle):
    basic_battle.play_turn(mode='player', debug=True)  
    assert len(basic_battle.player_party.get_alive_players()) == 2

def test_auto_turn(basic_battle):
    stats = basic_battle.play_turn(mode='auto', debug=True)
    assert stats
    assert stats.get(PlayerStat.attack, 0) >= 0

def test_enemy_turn(basic_battle):
    stats = basic_battle.play_turn(mode='enemy', debug=True, auto_play=True)
    assert stats
    assert stats.get(PlayerStat.attack, 0) >= 0
   
def test_combat_round(basic_battle):
    initial_hp = basic_battle.enemy_party.players[0].attr[PlayerStat.health]
    basic_battle.combat_round(debug=True, auto_play=True)
    final_hp = basic_battle.enemy_party.players[0].attr[PlayerStat.health]
    assert final_hp <= initial_hp
    
def test_start(basic_battle): 
    basic_battle.start_game(debug=True, auto_play=True)
    assert (basic_battle.player_party.get_alive_players() 
            or basic_battle.enemy_party.get_alive_players())
    
if __name__ == "__main__":
    sys.exit(pytest.main(["-v", "-s", "./api/game/gametests/test_battle.py"]))