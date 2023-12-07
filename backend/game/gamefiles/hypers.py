from game.gamefiles import g_vars
import random
import json
PlayerStat = g_vars.PlayerStat
ItemType = g_vars.ItemType

HYPERS_FILE = './api/game/gamefiles/hypers.json'

item_hypers = {
    ItemType.potion : 0.3,
    ItemType.magic : 0.6,
    ItemType.melee : 0.8,
    ItemType.ranged : 0.9,
    ItemType.armor : 0.7,
}

player_hypers = {
    PlayerStat.attack : 0.9,
    PlayerStat.defense : 0.8,
    PlayerStat.charisma : 0.3,
    PlayerStat.intelligence : 0.3,
    PlayerStat.wisdom : 0.3,
    PlayerStat.health : 0.98,
    PlayerStat.mana : 0.5,
    PlayerStat.stamina : 0.5,
    PlayerStat.level : 0.1,
}

meta_params = {
        "use_scale": 0.2
    }


def convert_keys(dc):
    if type(list(dc.keys())[0]) in [ItemType, PlayerStat]:
        dc = {key.value: val for key, val in dc.items()}
    else:
        dc = {PlayerStat(key) if list(dc.keys())[0] in [e.value for e in PlayerStat] else ItemType(int(key)): val for key, val in dc.items()}
    return dc

def save_hypers(item_hypers, player_hypers, meta_params):
    item_hypers = convert_keys(item_hypers)
    player_hypers = convert_keys(player_hypers)
    data = {
        'item_hypers': item_hypers,
        'player_hypers': player_hypers,
        'meta': meta_params
    }
    with open(HYPERS_FILE, 'w') as f: 
        json.dump(data, f)

def load_hypers(): 
    """Loads and returns the updated hypers from JSON"""
    with open(HYPERS_FILE) as f:
        data = json.load(f)
    item_hypers = convert_keys(data['item_hypers'])
    player_hypers = convert_keys(data['player_hypers'])
    meta_params = data['meta']
    return item_hypers, player_hypers, meta_params

def randomize(hyper_params):
    hyper_param = hyper_params.copy()
    for key, val in hyper_param.items():
        hyper_param[key] = round(random.uniform(0.01, 1), ndigits=2)
    return hyper_param
