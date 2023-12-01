import pytest
from auto_test_game import test_game_auto

tests = 300

lev = 10
@pytest.mark.parametrize("level, party_size , verbose, num_games, testing", [
    (lev, 1, False, tests, True),
    (lev, 2, False, tests, True),
    (lev, 3, False, tests, True),
    (lev, 4, False, tests, True), 
    (lev, 5, False, tests, True),
    (lev, 6, False, tests, True),   
])

def test_game_level_10(level, party_size , verbose, num_games, testing):
    test_game_auto(level, party_size , verbose, num_games, testing)
    
lev = 20
@pytest.mark.parametrize("level, party_size , verbose, num_games, testing", [
    (lev, 1, False, tests, True),
    (lev, 2, False, tests, True),
    (lev, 3, False, tests, True),
    (lev, 4, False, tests, True), 
    (lev, 5, False, tests, True),
    (lev, 6, False, tests, True),   
])

def test_game_level_20(level, party_size , verbose, num_games, testing):
    test_game_auto(level, party_size , verbose, num_games, testing)
    
lev = 40
@pytest.mark.parametrize("level, party_size , verbose, num_games, testing", [
    (lev, 1, False, tests, True),
    (lev, 2, False, tests, True),
    (lev, 3, False, tests, True),
    (lev, 4, False, tests, True), 
    (lev, 5, False, tests, True),
    (lev, 6, False, tests, True),   
])

def test_game_level_40(level, party_size , verbose, num_games, testing):
    test_game_auto(level, party_size , verbose, num_games, testing)
    
lev = 60
@pytest.mark.parametrize("level, party_size , verbose, num_games, testing", [
    (lev, 1, False, tests, True),
    (lev, 2, False, tests, True),
    (lev, 3, False, tests, True),
    (lev, 4, False, tests, True), 
    (lev, 5, False, tests, True),
    (lev, 6, False, tests, True),   
])

def test_game_level_60(level, party_size , verbose, num_games, testing):
    test_game_auto(level, party_size , verbose, num_games, testing)
    
lev = 80
@pytest.mark.parametrize("level, party_size , verbose, num_games, testing", [
    (lev, 1, False, tests, True),
    (lev, 2, False, tests, True),
    (lev, 3, False, tests, True),
    (lev, 4, False, tests, True), 
    (lev, 5, False, tests, True),
    (lev, 6, False, tests, True),   
])

def test_game_level_80(level, party_size , verbose, num_games, testing):
    test_game_auto(level, party_size , verbose, num_games, testing)
    
lev = 90
@pytest.mark.parametrize("level, party_size , verbose, num_games, testing", [
    (lev, 1, False, tests, True),
    (lev, 2, False, tests, True),
    (lev, 3, False, tests, True),
    (lev, 4, False, tests, True), 
    (lev, 5, False, tests, True),
    (lev, 6, False, tests, True),   
])

def test_game_level_90(level, party_size , verbose, num_games, testing):
    test_game_auto(level, party_size , verbose, num_games, testing)
    