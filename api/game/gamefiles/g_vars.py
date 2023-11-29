stats = ['ATK', 'DEF', 'CHA', 'INT', 'WIS', 'HP', 'MP', 'STA','LVL']
item_names = ['potion', 'magic', 'weapon', 'armor']
choices = {
    'potion': stats[:-1],
    'magic': stats[:-4],
    'weapon': stats[0],
    'armor': stats[1]
}