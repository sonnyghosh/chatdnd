from game.gamefiles import g_vars
PlayerStat = g_vars.PlayerStat

def agg(store, sample):
    store.update({key: store.get(key, 0) + val for key, val in sample.items()})
    return store

def colorize(text, color):
    colors = {
        'reset': '\033[0m',
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'purple': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m'
    }
    return f'{colors[color]}{text}{colors["reset"]}'

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