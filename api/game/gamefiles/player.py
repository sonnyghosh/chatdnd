import random
from . import item, g_vars
ItemType = g_vars.ItemType
PlayerStat = g_vars.PlayerStat
StatColor = g_vars.StatColor
config = g_vars.config
from game.gametests import utils
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

item_names = config['item']['names']

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
        self.get_rank()
    
    def get_rank(self):
        stat_rank = sum(self.stats.values())
        items_rank = sum([sum([i.rank for i in it]) for it in self.items.values()])
        attr_rank = sum([att for key, att in self.attr.items() if key != 'name'])
        self.rank = stat_rank + items_rank + attr_rank
        return stat_rank + items_rank + attr_rank

    def validate_player(self):
        # Validate stats
        for stat, value in self.stats.items():
            if not (0 <= value <= 50):
                print(f"Invalid {stat} value for {self.name} - {value}. Valid range: {range(0,50)}")
                return False

        # Validate attributes
        for attr, value in self.attr.items():
            if attr != 'name' and not (0 <= value <= 100):
                print(f"Invalid {attr} value for {self.name} - {value}. Valid range: {range(0,100)}")
                return False

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

    def get_item_type_str(self, itemtype, prefix='', spacer='\t'):
        res = f'{itemtype.name}\n'
        res += prefix
        for idx, itm in enumerate(self.get_item_type(itemtype=itemtype)):
            res += spacer
            res += f'{idx}. {itm}\n'
        return res

    def get_item_type(self, itemtype):
        return [w for w in self.items[itemtype] if ( w.uses != 0 and abs(w.effects.get(PlayerStat.stamina, 0)) <= self.attr[PlayerStat.stamina] and abs(w.effects.get(PlayerStat.mana, 0)) <= self.attr[PlayerStat.mana] )]

    def __str__(self) -> str:
        # print out the name of the player
        res = f'\t--------| {self.name} - {self.rank} |---------\n'

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
        res += self.get_item_type_str(ItemType.potion)
        res += self.get_item_type_str(ItemType.magic)
        res += '\n\t-------------------------'
        return res

    def get_dice_roll(self) -> tuple:
        min_roll = 0
        max_roll = 1 
        for stat in self.stats.values():
            min_roll += 0.02 * stat
            max_roll += 0.08 * stat
        return random.randint(int(min_roll), int(max_roll))

    def attack(self, target: 'Player', use_armor=True):
        return self.use_attack({PlayerStat.attack:0, PlayerStat.stamina: -random.randint(1,4)}, target, use_armor=use_armor)

    def use_attack(self, effects, target: 'Player', use_armor=True):
         # use item to get effects
        if effects:
            # get roles for players
            attacker_role = self.get_dice_roll()
            target_role = target.get_dice_roll()
            
        
            damage = self.stats[PlayerStat.attack] # Calculate base damage 
            damage += effects.get(PlayerStat.attack, 0)   # Add damage effects from item
            
            # chance for critical hit based on roll
            if 15 < attacker_role:
                damage *= 2
                print("Critical hit!")

            if use_armor:
                armor = target.get_item_type(ItemType.armor)
                if len(armor) > 0:
                    armor = armor[0]
                    block = armor.use()
                    print(f'{target.name} is using [{utils.colorize(str(block[PlayerStat.stamina])+" STA", StatColor.stamina.value)}] armor to add [{utils.colorize(str(block[PlayerStat.defense])+" DEF" , StatColor.defense.value)}]!') 
                    damage -= block[PlayerStat.defense]
                    target.attr[PlayerStat.stamina] += block[PlayerStat.stamina]

            damage -= int(target.stats[PlayerStat.defense]*(target.attr[PlayerStat.level]/100)) # Reduce damage based on target's defense 
            damage = max(5, damage) # Make sure damage is at least 1
            
            # chance to dodge based on role
            if target_role > 16:
                damage == 0 
                print("Attack Dodged!")

            target.attr[PlayerStat.health] = max(0, target.attr[PlayerStat.health] - damage) # Apply damage 
            sta_degredation = min(0,effects.get(PlayerStat.stamina, 0))
            self.attr[PlayerStat.stamina] += sta_degredation # reduce player stamina
            if effects.get(PlayerStat.attack, 0) == 0:
                print(f"{self.name} [{utils.colorize(str(target.attr[PlayerStat.stamina])+' STA', StatColor.stamina.value)}] Lost {utils.colorize(str(sta_degredation)+' STA', StatColor.stamina.value)} attacking {target.name} [{utils.colorize(str(target.attr[PlayerStat.health])+' HP', StatColor.health.value)}] for {utils.colorize( str(damage)+' ATK', StatColor.attack.value)}!") # Print attack message
            else:
                print(f"{self.name} [{utils.colorize(str(target.attr[PlayerStat.stamina])+' STA', StatColor.stamina.value)}] Lost {utils.colorize(str(sta_degredation)+' STA', StatColor.stamina.value)} attacking {target.name} [{utils.colorize(str(target.attr[PlayerStat.health])+' HP', StatColor.health.value)}] for {utils.colorize( str(damage)+' ATK', StatColor.attack.value)} with a \033[1m\033[4mweapon\033[0m!") # Print attack message
            return {PlayerStat.attack:damage, PlayerStat.stamina: sta_degredation}
        else:
            return self.attack(target=target)
    
    def use_magic(self, effects, target: 'Player'=None):
        if effects:
            player = target if target else self
            
            if PlayerStat.attack in effects.keys():
                attacker_role = self.get_dice_roll()
                target_role = player.get_dice_roll()

                damage = self.stats[PlayerStat.attack] # Calculate base damage 
                damage += effects.get(PlayerStat.attack, 0)   # Add damage effects from item

                if 17 < attacker_role:
                    damage *= 2
                    print("Critical hit!")

                damage -= player.stats[PlayerStat.defense] # Reduce damage based on target's defense 
                damage = max(1, damage) # Make sure damage is at least 1

                if target_role > 17:
                    damage == 0
                    print("Attack Dodged!")

                player.attr[PlayerStat.health] = max(0, player.attr[PlayerStat.health] - damage) # Apply damage
                self.attr[PlayerStat.mana] = max(0,self.attr[PlayerStat.mana] + effects.get(PlayerStat.mana, 0)) # reduce player stamina
                print(f"{self.name} [{utils.colorize(self.attr[PlayerStat.mana], StatColor.mana.value)}] used {utils.colorize(effects[PlayerStat.mana], StatColor.mana.value)} cast magic on {player.name} for {utils.colorize(damage, StatColor.attack.value)} damage!")

            else:
                buff = list(effects.keys())
                buff.remove(PlayerStat.mana)
                cost = effects[PlayerStat.mana]
                self.attr[PlayerStat.mana] += cost
                res = f'{self.name} used [{utils.colorize(str(cost), StatColor.mana.value)}] cast magic on {player.name} to give them ['
                for att in buff:
                    res += utils.colorize(f'+{effects[att]} {att.value}', PlayerStat(att).color().value)
                    if att in player.attr.keys():
                        player.attr[att] = min(100, effects[att] + player.attr[att])
                    elif att in player.stats.keys():
                        player.stats[att] = min(50, effects[att] + player.stats[att])
                print(res+']')
            
            return 0
        else:
            print('cannot use this spell')
            return 1

    def use_item(self, effects, target: 'Player'=None):
        res = ''
        if effects:
            player = target if target else self
            res += f'{player.name} recieved '
            for key, val in effects.items():
                res += utils.colorize(f'+{val} {key.value}', PlayerStat(key).color().value)
                if key in player.stats.keys():
                    player.stats[key] = min(50, val + player.stats[key])

                elif key in player.attr.keys():
                    player.attr[key] = min(100, val + player.attr[key])
        res += f' from {self.name}\'s potion!'
        print(res)

    def use(self, item, target: 'Player'=None, use_armor=True):
        effects = item.use()
        if item.type == ItemType.potion:
            self.use_item(effects, target)
        elif item.type == ItemType.magic:
            self.use_magic(effects, target)
        elif item.type == ItemType.weapon:
            return self.use_attack(effects, target, use_armor=use_armor)
        if item.uses == 0 and item in self.items[item.type]:
            self.items[item.type].remove(item)
        return effects

    def give(self, item: item.Item, target: 'Player'):
        temp = item
        self.items[item.type].remove(item)
        target.items[item.type].append(temp)
        print(f'{self.name} gave {target.name} - {utils.colorize(item.type.name, ["bold", "cyan", "on_black"])}')

    def sort_inv(self):
        for item_list in self.items.values():
            item_list.sort(key=lambda x: (x.rank, next(iter(x.effects.values()))), reverse=True)
        return self

def generate_player(name, level=None):
    attr = {
        PlayerStat.level: level if level else random.randint(25,100),
        PlayerStat.health: 100,
        PlayerStat.mana: 100,
        PlayerStat.stamina: 100,
        'name': name,
    }

    stats = {
        PlayerStat.attack: min(50,int(random.randint(1+int(attr[PlayerStat.level]/5),1+int(attr[PlayerStat.level]/1.75)))),
        PlayerStat.defense: min(50,int(random.randint(1+int(attr[PlayerStat.level]/5),1+int(attr[PlayerStat.level]/1.75)))),
        PlayerStat.charisma: min(50,int(random.randint(1+int(attr[PlayerStat.level]/5),1+int(attr[PlayerStat.level]/1.75)))),
        PlayerStat.intelligence: min(50,int(random.randint(1+int(attr[PlayerStat.level]/5),1+int(attr[PlayerStat.level]/1.75)))),
        PlayerStat.wisdom: min(50,int(random.randint(1+int(attr[PlayerStat.level]/5),1+int(attr[PlayerStat.level]/1.75))))
    }

    items = item.generate_items(random.randint(12,18), attr[PlayerStat.level])
    return Player(stats=stats, attr=attr, items=items).sort_inv()