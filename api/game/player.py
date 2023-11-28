import random
from game import item
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
        'STA': 0-100,
        'name': str,
    }

    items = [Item()...]
    '''
    def __init__(self, stats, attr, items):
        self.name = attr['name']
        self.stats = stats
        self.attr = attr
        self.items = items
    
    def __str__(self) -> str:
        # print out the name of the player
        res = f'\t--------| {self.name} |---------\n'

        # print all of the player stats
        res += '\tStats:'
        for st, val in self.stats.items():
            res += f'\n\t\t{st} - {val}'

        # print out the attributes of th player
        res += '\n\tAttributes:'
        for st, val in self.attr.items():
            res += f'\n\t\t{st} - {val}'

        #print out player items
        res += '\n\tItems:'
        for idx, it in enumerate(self.items):
            res += f'\n\t\t{idx}: {it}'

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

            damage -= target.stats["DEF"] # Reduce damage based on target's defense 
            damage = max(1, damage) # Make sure damage is at least 1
            
            # chance to dodge based on role
            if target_role > 16:
                damage == 0
                print("Attack Dodged!")

            target.attr["HP"] -= damage # Apply damage 
            self.attr['STA'] += effects.get('STA', 0) - 5 # reduce player stamina
            print(f"{self.name} attacked {target.name} for {damage} damage!") # Print attack message
            return 0
        else:
            print('This weapon cant be used')
            return 1
    
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

                player.attr["HP"] -= damage # Apply damage
                self.attr['MP'] += effects.get('MP', 0) - 5 # reduce player stamina
                print(f"{self.name} cast magic on {player.name} for {damage} damage!")
            else:
                buff = list(effects.keys())
                buff.remove('MP')
                cost = effects['MP']
                self.attr['MP'] += cost
                for att in buff:
                    if att in player.attr.keys():
                        player.attr[att] += effects[att]
                    elif att in player.stats.keys():
                        player.stats[att] += effects[att]

            
            return 0
        else:
            print('cannot use this spell')
            return 1

    def use_item(self, effects, target=None):
        if effects:
            player = target if target else self
            for key, val in effects.items():
                if key in player.stats.keys():
                    player.stats[key] += val

                elif key in player.attr.keys():
                    player.attr[key] += val

    def use(self, item, target=None):
        effects = item.use()
        if item.cat == 0:
            self.use_item(effects, target)
        elif item.cat == 1:
            self.use_magic(effects, target)
        elif item.cat == 2:
            self.use_attack(effects, target)