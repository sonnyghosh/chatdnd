import pytest
from auto_test_game import test_game_auto

tests = 100

lev = 10
@pytest.mark.parametrize("level, party_size, num_games, testing", [
    (lev, 1, tests, True),
    (lev, 2, tests, True),
    (lev, 3, tests, True),  
])

def test_game_level_10(level, party_size, num_games, testing):
    test_game_auto(level, party_size, num_games, testing)
    
lev = 20
@pytest.mark.parametrize("level, party_size, num_games, testing", [
    (lev, 2, tests, True),
    (lev, 3, tests, True),
    (lev, 4, tests, True),  
])

def test_game_level_20(level, party_size, num_games, testing):
    test_game_auto(level, party_size, num_games, testing)
    
lev = 40
@pytest.mark.parametrize("level, party_size, num_games, testing", [
    (lev, 2, tests, True),
    (lev, 3, tests, True),
    (lev, 4, tests, True),
    (lev, 5, tests, True),  
])

def test_game_level_40(level, party_size, num_games, testing):
    test_game_auto(level, party_size, num_games, testing)
    
lev = 60
@pytest.mark.parametrize("level, party_size, num_games, testing", [
    (lev, 4, tests, True),
    (lev, 5, tests, True),  
    (lev, 6, tests, True),  
])

def test_game_level_60(level, party_size, num_games, testing):
    test_game_auto(level, party_size, num_games, testing)
    
lev = 80
@pytest.mark.parametrize("level, party_size, num_games, testing", [
    (lev, 4, tests, True),
    (lev, 5, tests, True),  
    (lev, 6, tests, True),  
])

def test_game_level_80(level, party_size, num_games, testing):
    test_game_auto(level, party_size, num_games, testing)
    
lev = 90
@pytest.mark.parametrize("level, party_size, num_games, testing", [
    (lev, 4, tests, True),
    (lev, 5, tests, True),  
    (lev, 6, tests, True),  
])

def test_game_level_90(level, party_size, num_games, testing):
    test_game_auto(level, party_size, num_games, testing)
    