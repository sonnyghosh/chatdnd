from game.gamefiles import g_vars
PlayerStat = g_vars.PlayerStat
import os

dataset_file = "./api/game/gamefiles/data/dataset.txt"

def clr_t():
    os.system('cls' if os.name == 'nt' else 'clear')

def agg(store, sample):
    store.update({key: store.get(key, 0) + val for key, val in sample.items()})
    return store

def colorize(text, color_list):
    color_list = color_list if type(color_list) is list else [color_list]
    colors = {
        # default
        'reset': '\033[0m',  
        # styles 
        'bold': '\033[1m',
        'underline': '\033[4m',
        'invert': '\033[7m',

        # text colors 
        'black': '\033[30m',
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m',

        # background colors
        'on_black': '\033[40m', 
        'on_red': '\033[41m',
        'on_green': '\033[42m',
        'on_yellow': '\033[43m',  
        'on_blue': '\033[44m',
        'on_magenta': '\033[45m', 
        'on_cyan': '\033[46m',
        'on_white': '\033[47m',  

        # bright colors
        'bright_black': '\033[90m',
        'bright_red': '\033[91m',
        'bright_green': '\033[92m',
        'bright_yellow': '\033[93m',
        'bright_blue': '\033[94m',
        'bright_magenta': '\033[95m',
        'bright_cyan': '\033[96m',
        'bright_white': '\033[97m',

        # bright background 
        'on_bright_black': '\033[100m',
        'on_bright_red': '\033[101m',  
        'on_bright_green': '\033[102m',
        'on_bright_yellow': '\033[103m',
        'on_bright_blue': '\033[104m',
        'on_bright_magenta': '\033[105m',
        'on_bright_cyan': '\033[106m',
        'on_bright_white': '\033[107m'  
    }
    return f'{"".join([colors[c] for c in color_list])}{text}{colors["reset"]}'

def summarize(title, dicti, games=1):
    A = [PlayerStat.attack,PlayerStat.attack,PlayerStat.stamina,PlayerStat.stamina,PlayerStat.mana,PlayerStat.mana,PlayerStat.health,PlayerStat.health]
    B = ["turns","moves","turns","moves","turns","moves","turns","moves"]
    print(colorize(f'{title}:', 'blue'))
    res = ''
    item_num = 0
    for key, val in dicti[title].items():
        res += f'\t{colorize(f"AVG {key if type(key) is str else key.name}", "white")} - \t{colorize(f"Total:{val} - Avg:{val/games}", "red" if val < 0 else "green")}'
        if item_num % 3 == 2:
            res += '\n'
        item_num += 1
    print(res)
    res = ''
    item_num = 0
    for a, b in zip(A,B):
        val = dicti[title][a]/dicti[title][b]
        res += f'\t{colorize(f"{a.name}/{b}", "white")} : {colorize(round(val, ndigits=2), "red" if val < 0 else "green")}'
        if item_num % 2 == 1:
            res += '\n'
        item_num += 1
    print(res)

def cross_stats(stats):
    pl = stats['Player']
    en = stats['Enemy']
    print('\nCross stats:')
    print('Player stats:')
    print('give/move:', colorize(f'{round(pl["give"]/pl["moves"], ndigits=4)}', 'red' if pl["give"]/pl["moves"] > 0.1 else 'green'), end='\t')
    print('pass/move:', colorize(f'{round(pl["pass"]/pl["moves"], ndigits=4)}', 'red' if pl["pass"]/pl["moves"] > 0.15 else 'green'), end='\t')
    print('buff/move:', colorize(f'{round(pl["buff"]/pl["moves"], ndigits=4)}', 'red' if pl["buff"]/pl["moves"] > 0.3 else 'green'), end='\t')
    print('magic/move:', colorize(f'{round(pl["magic"]/pl["moves"], ndigits=4)}', 'red' if pl["magic"]/pl["moves"] < 0.05 else 'green'), end='\t')
    print('weapon/move:', colorize(f'{round(pl["weapon"]/pl["moves"], ndigits=4)}', 'red' if pl["weapon"]/pl["moves"] < 0.45 else 'green'), end='\t')
    print('fist/move:', colorize(f'{round(pl["fist"]/pl["moves"], ndigits=4)}\n', 'red' if pl["fist"]/pl["moves"] > 0.1 else 'green'))

    print('Enemy Stats:')
    print('give/move:', colorize(f'{round(en["give"]/en["moves"], ndigits=4)}', 'red' if en["give"]/en["moves"] > 0.1 else 'green'), end='\t')
    print('pass/move:', colorize(f'{round(en["pass"]/en["moves"], ndigits=4)}', 'red' if en["pass"]/en["moves"] > 0.15 else 'green'), end='\t')
    print('buff/move:', colorize(f'{round(en["buff"]/en["moves"], ndigits=4)}', 'red' if en["buff"]/en["moves"] < 0.15 else 'green'), end='\t')
    print('magic_atk/move:', colorize(f'{round(en["magic"]/en["moves"], ndigits=4)}', 'red' if en["magic"]/en["moves"] < 0.05 else 'green'), end='\t')
    print('weapon/move:', colorize(f'{round(en["weapon"]/en["moves"], ndigits=4)}', 'red' if en["weapon"]/en["moves"] < 0.45 else 'green'), end='\t')
    print('fist/move:', colorize(f'{round(en["fist"]/en["moves"], ndigits=4)}\n', 'red' if en["fist"]/en["moves"] > 0.1 else 'green'))

    print('Avg Player Turns: ', pl['turns']/(pl['Wins'] + en['Wins']))
    print('Avg Player Moves: ', pl['moves']/(pl['Wins'] + en['Wins']))
    print(colorize('Player W/L:', 'white'), colorize(f'{round(pl["Wins"]/(pl["Losses"] + pl["Wins"]), ndigits=2)}', 'green' if 0.6 > pl["Wins"]/(pl["Losses"] + pl["Wins"]) > 0.4 else 'red'))
    print(colorize('Enemy W/L:', 'white'), colorize(f'{round(en["Wins"]/(en["Losses"] + en["Wins"]), ndigits=2)}', 'green' if 0.6 > en["Wins"]/(en["Losses"] + en["Wins"]) > 0.4 else 'red'))
    print('Player HP - Enemy ATK:', colorize(f'{pl[PlayerStat.health] - en[PlayerStat.attack]}', 'red' if pl[PlayerStat.health] - en[PlayerStat.attack] > 0 else 'green'))
    print('Enemy HP - Player ATK:', colorize(f'{en[PlayerStat.health] - pl[PlayerStat.attack]}', 'red' if en[PlayerStat.health] - pl[PlayerStat.attack] > 0 else 'green'))
    print('power level ratio:', colorize(f'{round(pl["power"]/en["power"], ndigits=2)}', 'green' if 1.2 > pl["power"]/en["power"] > 0.8 else 'red'))