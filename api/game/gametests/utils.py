from game.gamefiles import g_vars
PlayerStat = g_vars.PlayerStat

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

def summarize(title, dicti, games=1, classes=1):
    A = [PlayerStat.attack,PlayerStat.attack,PlayerStat.stamina,PlayerStat.stamina,PlayerStat.mana,PlayerStat.mana,PlayerStat.health,PlayerStat.health]
    B = ["turns","moves","turns","moves","turns","moves","turns","moves"]
    print(colorize(f'{title}:', 'blue'))
    for key, val in dicti[title].items():
        print(f'\t{colorize(f"AVG {key if type(key) is str else key.name}", "white")} - {colorize(f"Total:{val} - Avg:{val/(games/classes)}", "red" if val < 0 else "green")}')
    for a, b in zip(A,B):
        val = dicti[title][a]/dicti[title][b]
        print(f'\t{colorize(f"{a.name}/{b}", "white")} : {colorize(round(val, ndigits=2), "red" if val < 0 else "green")}')

def cross_stats(stats):
    pl = stats['Player']
    en = stats['Enemy']
    print('\nCross stats:')
    print(colorize('Player_W / Enemy_W:', 'white'), colorize(f'{pl["Wins"]/en["Wins"]}', 'red' if pl["Wins"]/en["Wins"] < 1 else 'green'))
    print('Player HP - Enemy ATK:', colorize(f'{pl[PlayerStat.health] - en[PlayerStat.attack]}', 'red' if pl[PlayerStat.health] - en[PlayerStat.attack] < 0 else 'green'))
    print('Enemy HP - Player ATK:', colorize(f'{en[PlayerStat.health] - pl[PlayerStat.attack]}', 'red' if en[PlayerStat.health] - pl[PlayerStat.attack] < 0 else 'green'))