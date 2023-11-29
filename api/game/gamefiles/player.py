import random
from . import item

"""
Item Documentation:
    Represents an item in a video game.

    Attributes:
    - name (str): The name of the item.
    - uses (int): The number of uses the item has.
    - effects (dict): A dictionary representing the effects of the item on game stats.

    Methods:
    - use(): Applies the effects of the item and decrements its uses. If uses reach 0, the item is broken.
            - returns dict of effects {str:'stat/attr': int:value, ...}
    """

item_names = ['potion', 'magic', 'weapon', 'armor']

class Player:
    '''
    These are all of the stats for the players they are organized in 3 different areas based on type
    stats = {
        'ATK': 0-50,
        'DEF': 0-50,
        'CHA': 0-50,
        'INT': 0-50,
        'WIS': 0-50
    }

    attr = {
        'LVL': 0-100,
        'HP': 0-100,
        'MP': 0-100,
        'STA': 0-100,
        'name': str,
    }

    items = {
        'potions' 0: [Item(type=0)...],
        'magic' 1: [Item(type=1)...],
        'weapons' 2:[Item(type=2)...],
        'armor' 3: [Item(type=3)...]
    }
    '''
    def __init__(self, stats, attr, items):
        self.name = attr['name']
        self.stats = stats
        self.attr = attr
        self.items = items
        self.usable_items = True
    
    def validate_player(self):
        # Validate stats
        for stat, value in self.stats.items():
            if not (0 <= value <= 50):
                raise ValueError(f"Invalid {stat} value for {self.name} - {value}. Valid range: {range(0,50)}")

        # Validate attributes
        for attr, value in self.attr.items():
            if attr != 'name' and not (0 <= value <= 100):
                raise ValueError(f"Invalid {attr} value for {self.name} - {value}. Valid range: {range(0,100)}")

        # Validate items
        for item_type, item_list in self.items.items():
            for item in item_list:
                good = item.validate_effects() 
                if not good: return False
        return True

    def get_items_str(self):
        spacer = '\n\t'
        res = spacer
        res += f'Items:'
        spacer += '  '
        for typ, lst in self.items.items():
            res += f'\n\t{item_names[typ]}:{spacer}{"".join([str(x) + spacer for x in lst if x.uses != 0])}'
        return res

    def get_weapons(self):
        return [w for w in self.items[2] if w.uses != 0]

    def get_item_ind(self, ind):
        return [w for w in self.items[ind] if w.uses != 0]

    def get_weapons_str(self, spacer='\t'):
        res = f'Weapons:\n'
        for idx, itm in enumerate(self.get_weapons()):
            res += spacer
            res += f'{idx}. {itm}\n'
        return res
    
    def get_armor_str(self, spacer = '\t'):
        res = f'Armor:\n'
        for idx, itm in enumerate(self.items[3]):
            res += f'{spacer}{idx}. {itm}\n'
        return res
    
    def get_potions_str(self):
        spacer = '\n\t'
        res = f'{spacer}0) Potions:'
        spacer += '  '
        for idx, itm in enumerate(self.items[0]):
            res += f'{spacer}{idx}. {itm}'
        return res
    
    def get_magic_str(self):
        spacer = '\n\t'
        res = f'{spacer}1) Magic:'
        spacer += '  '
        for idx, itm in enumerate(self.items[1]):
            res += f'{spacer}{idx}. {itm}'
        return res

    def __str__(self) -> str:
        # print out the name of the player
        res = f'\t--------| {self.name} |---------\n'

        # print all of the player stats
        res += '\tStats:'
        for st, val in self.stats.items():
            res += f'| {st} - {val} '
        res += '|'
        # print out the attributes of th player
        res += '\n\tAttributes:'
        for st, val in self.attr.items():
            res += f'| {st} - {val} '
        res += '|'
        #print out player items
        res += '\n\tItems:'
        res += self.get_potions_str()
        res += self.get_magic_str()
        res += '\n\t-------------------------'
        return res

    def get_dice_roll(self) -> tuple:
        min_roll = 0
        max_roll = 1 
        for stat in self.stats.values():
            min_roll += 0.02 * stat
            max_roll += 0.08 * stat
        return random.randint(int(min_roll), int(max_roll))

    def attack(self, target):
        return self.use_attack({'ATK':0, 'STA': -random.randint(1,4)}, target)

    def use_attack(self, effects, target):
         # use item to get effects
        if effects:
            # get roles for players
            attacker_role = self.get_dice_roll()
            target_role = target.get_dice_roll()
            
        
            damage = self.stats["ATK"] # Calculate base damage 
            damage += effects.get("ATK", 0)   # Add damage effects from item
            
            # chance for critical hit based on roll
            if 15 < attacker_role:
                damage *= 2
                print("Critical hit!")

            damage -= int(target.stats["DEF"]*(target.attr['LVL']/100)) # Reduce damage based on target's defense 
            damage = max(1, damage) # Make sure damage is at least 1
            
            # chance to dodge based on role
            if target_role > 16:
                damage == 0
                print("Attack Dodged!")

            target.attr["HP"] = max(0, target.attr["HP"] - damage) # Apply damage 
            sta_degredation = effects.get('STA', 0) - random.randint(1,4)
            self.attr['STA'] += sta_degredation # reduce player stamina
            if effects.get('ATK', 0) == 0:
                print(f"{self.name} [{target.attr['STA']} STA] Lost {sta_degredation} STA attacking {target.name} [{target.attr['HP']} HP] for {damage} damage!") # Print attack message
            else:
                print(f"{self.name} [{target.attr['STA']} STA] Lost {sta_degredation} STA attacking {target.name} [{target.attr['HP']} HP] for {damage} damage with a weapon!") # Print attack message
            return damage, sta_degredation
        else:
            return self.attack(target=target)
    
    def use_magic(self, effects, target=None):
        if effects:
            player = target if target else self
            
            if 'ATK' in effects.keys():
                attacker_role = self.get_dice_roll()
                target_role = player.get_dice_roll()

                damage = self.stats["ATK"] # Calculate base damage 
                damage += effects.get("ATK", 0)   # Add damage effects from item

                if 17 < attacker_role:
                    damage *= 2
                    print("Critical hit!")

                damage -= player.stats["DEF"] # Reduce damage based on target's defense 
                damage = max(1, damage) # Make sure damage is at least 1

                if target_role > 17:
                    damage == 0
                    print("Attack Dodged!")

                player.attr["HP"] = max(0, player.attr['HP'] - damage) # Apply damage
                self.attr['MP'] = max(0,self.attr['MP'] + effects.get('MP', 0) - 5) # reduce player stamina
                print(f"{self.name} cast magic on {player.name} for {damage} damage!")

            else:
                buff = list(effects.keys())
                buff.remove('MP')
                cost = effects['MP']
                self.attr['MP'] += cost
                res = f'{self.name} cast magic on {player.name} to give them '
                for att in buff:
                    res += f'+{effects[att]} {att} '
                    if att in player.attr.keys():
                        player.attr[att] = min(100, effects[att] + player.attr[att])
                    elif att in player.stats.keys():
                        player.stats[att] = min(50, effects[att] + player.stats[att])
                print(res)
            
            return 0
        else:
            print('cannot use this spell')
            return 1

    def use_item(self, effects, target=None):
        res = ''
        if effects:
            player = target if target else self
            res += f'{player.name} recieved '
            for key, val in effects.items():
                res += f'+{val} {key} '
                if key in player.stats.keys():
                    player.stats[key] = min(50, val + player.stats[key])

                elif key in player.attr.keys():
                    player.attr[key] = min(100, val + player.attr[key])
        res += f'from {self.name}\'s potion!'
        print(res)

    def use(self, item, target=None):
        effects = item.use()
        if item.cat == 0:
            self.use_item(effects, target)
        elif item.cat == 1:
            self.use_magic(effects, target)
        elif item.cat == 2:
            self.use_attack(effects, target)
        return effects

def generate_player(name, level=None):
    attr = {
        'LVL': level if level else random.randint(25,100),
        'HP': 100,
        'MP': 100,
        'STA': 100,
        'name': name,
    }

    stats = {
        'ATK': min(50,int(random.randint(1+int(attr['LVL']/5),1+int(attr['LVL']/1.75)))),
        'DEF': min(50,int(random.randint(1+int(attr['LVL']/5),1+int(attr['LVL']/1.75)))),
        'CHA': min(50,int(random.randint(1+int(attr['LVL']/5),1+int(attr['LVL']/1.75)))),
        'INT': min(50,int(random.randint(1+int(attr['LVL']/5),1+int(attr['LVL']/1.75)))),
        'WIS': min(50,int(random.randint(1+int(attr['LVL']/5),1+int(attr['LVL']/1.75))))
    }

    items = item.generate_items(random.randint(12,18), attr['LVL'])
    return Player(stats=stats, attr=attr, items=items)