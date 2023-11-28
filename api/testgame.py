import random
import sys
sys.path.append('./api/game')
from game import battle, item, player, party

stats = ['ATK', 'DEF', 'CHA', 'INT', 'WIS', 'HP', 'MP', 'STA','LVL']
item_names = ['potion', 'magic', 'weapon']
choices = {
    'potion': stats[:-1],
    'magic': stats[:-4],
    'weapon': stats[0],
}

def generate_items(n_items):
    bag = []
    for _ in range(n_items):
        ind = random.randint(0,2)
        if ind == 0:
            bag.append(item.Item(item_names[ind],
                                 ind, 
                                 random.randint(1,4), 
                                 {random.choice(choices[item_names[ind]]): random.randint(5,25)}))
        elif ind == 1:
            bag.append(item.Item(item_names[ind],
                                 ind, 
                                 random.randint(1,3), 
                                 {random.choice(choices[item_names[ind]]): random.randint(10,35),
                                  'MP': random.randint(-15,-1)}))
        elif ind == 2:
            bag.append(item.Item(item_names[ind],
                                 ind, 
                                 random.randint(10,50), 
                                 {choices[item_names[ind]]: random.randint(20,45),
                                  'STA': random.randint(-15,-1)}))
    return bag

def generate_player(name):
    stats = {
        'ATK': random.randint(1,51),
        'DEF': random.randint(1,51),
        'CHA': random.randint(1,51),
        'INT': random.randint(1,51),
        'WIS': random.randint(1,51)
    }

    attr = {
        'LVL': random.randint(1,101),
        'HP': 100,
        'MP': 100,
        'STA': 100,
        'name': name,
    }

    items = generate_items(random.randint(3,7))

    return player.Player(stats=stats, attr=attr, items=items)

names = ["Blaze", "Rebel", "Ace", "Rogue", "Phoenix", "Echo", "Zenith", "Valor", "Cipher", "Nova", "Trinity", "Neo", "Onyx", "Astra", "Azure", "Bex", "Briar", "Cove", "Halo", "Ivory", "Jupiter", "Kai", "Lev", "Nyx", "Reign", "Rune", "Wren", "Zephyr"]

def generate_party(n_members, squad_name):
    members = []
    for _ in range(n_members):
        nm = random.choice(names)
        pl = generate_player(nm)
        members.append(pl)
    return party.Party(members, name=squad_name)

player_party = generate_party(1, 'Dike Tyson\'s Squad')
print(player_party)
enemy_party = generate_party(1, 'Enemy Squad')
print(enemy_party)
current_battle = battle.Battle(player_party, enemy_party)
current_battle.start()