import random
import sys
import os
import cProfile
from contextlib import redirect_stdout
CURRENT_DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.dirname(CURRENT_DIR)
sys.path.append(os.path.dirname(PARENT_DIR))
from game.gamefiles import battle, party, g_vars, test_character
from game.gametests import utils


def test_game(party_size, level, generate_party, testing=False):
    st = {
        'Player':{},
        'Enemy':{}
    }
    level_avg = level
    level_sd = 4
    if generate_party:
        player_party = party.generate_party(party_size if type(party_size) is int else party_size[0], 'Dike Tyson\'s Squad', avg_level=level_avg if type(level_avg) is int else level_avg[0], level_sd=level_sd)
        enemy_party = party.generate_party(party_size if type(party_size) is int else party_size[1], 'Enemy Squad', avg_level=level_avg if type(level_avg) is int else level_avg[1], level_sd=level_sd)
    else:
        player_party = test_character.Dike_Tyson_Party
        enemy_party = test_character.Enemy_Test_Party
    
    player_power = player_party.get_power_level()
    enemy_power = enemy_party.get_power_level()
    st['Player'] = utils.agg(st['Player'], {'power':player_power})
    st['Enemy'] = utils.agg(st['Enemy'], {'power':enemy_power})
    current_battle = battle.Battle(player_party, enemy_party)
    battle_stats = current_battle.start_game(auto_play=True, save_data=False) # make save data true to create dataset file link in utils
    st['Player'] = utils.agg(st['Player'], battle_stats[0])
    st['Enemy'] = utils.agg(st['Enemy'], battle_stats[1])
    return st, player_power/enemy_power, st['Player'].get('Wins', 0)

def test_game_auto(level=50, party_size = 1, num_games=200, testing=False):  
    master_stats = {
        'Player':{},
        'Enemy':{}
    }

    for _ in range(num_games):
        result,_,_ = test_game(party_size, level, generate_party=True, testing=True)
        master_stats['Player'] = utils.agg(master_stats['Player'], result['Player'])
        master_stats['Enemy'] = utils.agg(master_stats['Enemy'], result['Enemy'])

    assert master_stats['Player']['turns']/num_games < 30 if level <= 60 else 50, f"Game too long: {master_stats['Player']['turns']/num_games} turn avg"
    assert master_stats['Player']['Wins'] + master_stats['Enemy']['Wins'] == num_games , 'Too many games'
    assert 0.65 >= master_stats['Player']['Wins'] /num_games >= 0.35, f"W/L: {master_stats['Player']['Wins'] /num_games}"
    
def auto_test_levels(party_size, num_games, levels):
    master_stats = {ind : {'Player':{},'Enemy':{}} for ind in levels}

    if type(party) is tuple:
        size_a = random.choice(party_size)
        size_b = random.choice(party_size)
    else:
        size_a = party_size
        size_b = party_size

    for level in master_stats.keys():
        print('Starting Level', level)
        #utils.clr_t()
        for idx in range(num_games):
            #print('game:',idx)
            result, _, _ = test_game(party_size=(size_a, size_b), level=(level, level+random.randint(-3,4)), generate_party=True)
            master_stats[level]['Player'] = utils.agg(master_stats[level]['Player'], result['Player'])
            master_stats[level]['Enemy'] = utils.agg(master_stats[level]['Enemy'], result['Enemy'])

    for level in master_stats.keys():
        print('Avg Level:', level, end='\n')
        #utils.summarize('Player', master_stats[level], num_games)
        #utils.summarize('Enemy', master_stats[level], num_games)
        utils.cross_stats(master_stats[level])
    return master_stats

if False:
    for ps in range(1,3):
        pt_a = ps+1
        print(f'{ps} vs {pt_a}:')
        auto_test_levels(party_size=(ps, pt_a), num_games=60, levels=range(5,31, 5))

    for ps in range(2,4):
        pt_a = ps+1
        print(f'{ps} vs {pt_a}:')
        auto_test_levels(party_size=(ps, pt_a), num_games=40, levels=range(30,71, 5))

    for ps in range(3,6):
        pt_a = ps+1
        print(f'{ps} vs {pt_a}:')
        auto_test_levels(party_size=(ps, pt_a), num_games=20, levels=range(70,91, 5))

if False:
    p_s = 3
    lev = [10]
    num_g = 2

    cProfile.run('auto_test_levels(p_s, num_g, lev)')

if __name__ == '__main__':
    auto_test_levels(3, 10, [20, 50, 80])