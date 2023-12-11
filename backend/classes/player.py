import random
from . import item, class_utils
db = class_utils.db
from backend.game.gamefiles import g_vars, hypers
ItemType = g_vars.ItemType
PlayerStat = g_vars.PlayerStat
StatColor = g_vars.StatColor
config = g_vars.config
item_hypers, player_hypers, meta_params = hypers.load_hypers()
from game.gametests import utils
verbose = g_vars.config['meta']['verbose']
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
        <PlayerStat.attack,'ATK'>: 0-50,
        <PlayerStat.attack,'DEF'>: 0-50,
        <PlayerStat.attack,'CHA'>: 0-50,
        <PlayerStat.attack,'INT'>: 0-50,
        <PlayerStat.attack,'WIS'>: 0-50
    }

    attr = {
        <PlayerStat.level,'LVL'>: 0-100,
        <PlayerStat.health,'HP'>: 0-100,
        <PlayerStat.mana,'MP'>: 0-100,
        <PlayerStat.stamina,'STA'>: 0-100,
        'name': str,
    }

    items = {
        <ItemType.potion, 0>: [Item(ItemType=0)...],
        <ItemType.magic, 1>: [Item(ItemType=1)...],
        <ItemType.melee, 3>: [Item(ItemType=3)...],
        <ItemType.ranged, 4>: [Item(ItemType=4)...],
        <ItemType.armor, 2>: [Item(type=2)...]
    }
    '''
    def __init__(self, stats, attr, items):
        self.name = attr['name']
        self.stats = stats
        self.attr = attr
        self.items : dict = items
        self.usable_items = True
        self.rank = self.get_rank()
        self.id = class_utils.generate_id()
    
    def get_rank(self):
        if self.attr.get(PlayerStat.health,0) > 0:
            stat_rank = sum([player_hypers[key] * val for key, val in self.stats.items()])/max(1,len(self.stats.values()))
            items_rank = sum([sum([i.rank for i in it])/max(1,len(it)) for it in self.items.values()])/max(1,len(self.items))
            attr_rank = sum([player_hypers[key] * att for key, att in self.attr.items() if key != 'name'])/(len(self.attr)-1)
            self.rank = round(float((stat_rank + items_rank) * attr_rank)/10, ndigits=2)
        else:
            self.rank = 0
        return self.rank

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

    def get_item_type_str(self, itemtype, prefix='', spacer='\t', numbered=False):
        if prefix != '':
            prefix += ') '
        res = f'{prefix}{itemtype.name}\n'
        for idx, itm in enumerate(self.get_item_type(itemtype=itemtype)):
            res += spacer
            if numbered:
                res += f'{idx}. {itm}\n'
            else:
                res += f'{itm}\n'
        return res

    def get_item_type(self, itemtype):
        return [w for w in self.items[itemtype] if ( w.uses != 0 and abs(w.effects.get(PlayerStat.stamina, 0)) <= self.attr[PlayerStat.stamina] and abs(w.effects.get(PlayerStat.mana, 0)) <= self.attr[PlayerStat.mana] )]

    def get_top_n_item(self, itemtype, n):
        items = self.get_item_type(itemtype)
        if len(items) > 0:
            return items[0: min(len(items), n)]
        else:
            return items

    def __str__(self) -> str:
        # print out the name of the player
        res = f'\t--------| {self.name} - {self.rank} |---------\n'

        # print all of the player stats
        res += '\tStats:'
        for st, val in self.stats.items():
            res += f'| {st.name} - {val} '
        res += '|'
        # print out the attributes of th player
        res += '\n\tAttributes:'
        for st, val in self.attr.items():
            res += f'| {st.name if type(st) is PlayerStat else st} - {val} '
        res += '|'
        #print out player items
        res += '\n\tItems:\n'
        res += self.get_item_type_str(ItemType.potion, prefix='0:', numbered=False)
        res += self.get_item_type_str(ItemType.magic, prefix='1:', numbered=False)
        res += '\n\t-------------------------'
        return res

    def get_dice_roll(self, ranged=False) -> tuple:
        min_roll = 0
        max_roll = 1 + int(self.attr[PlayerStat.level]/5)
        roll = random.randint(int(min_roll), int(max_roll))

        if max_roll == 1:
            if roll == 1:
                return roll
            else:
                return -1
        
        elif roll >= int(max_roll *0.9):
            return -2
        
        elif ranged and (roll in [0,1] or roll == 0):
            return -1
        else:
            return roll
            
    def attack(self, target: 'Player', use_armor=True):
        return self.use_attack({PlayerStat.attack:0, PlayerStat.stamina: -random.randint(1,4)}, ItemType.melee, target, use_armor=use_armor)

    def use_attack(self, effects, itemtype, target: 'Player', use_armor=True):
         # use item to get effects
        if effects:
            range_weapon = True if itemtype == ItemType.ranged else False
            # get roles for players
            attacker_roll = self.get_dice_roll(range_weapon) # -2 - 20
            target_roll = target.get_dice_roll() # -2 - 20

            damage = self.stats[PlayerStat.attack] # Calculate base damage 
            damage += effects.get(PlayerStat.attack, 0)   # Add damage effects from item
            damage -= int(target.stats[PlayerStat.defense]*(target.attr[PlayerStat.level]/100)) # Reduce damage based on target's defense
            if use_armor:
                armor = target.get_item_type(ItemType.armor)
                if len(armor) > 0:
                    armor = armor[0]
                    block = armor.use()
                    if verbose:
                        print(f'{target.name} is using [{utils.colorize(str(block[PlayerStat.stamina])+" STA", StatColor.stamina.value)}] armor to add [{utils.colorize(str(block[PlayerStat.defense])+" DEF" , StatColor.defense.value)}]!') 
                    damage -= block[PlayerStat.defense]
                    target.attr[PlayerStat.stamina] = max(0, block[PlayerStat.stamina] + target.attr[PlayerStat.stamina])
            damage = max(5, damage)
            # chance for critical hit based on roll
            mult = round(random.random() + 1.1, ndigits=2)
            if attacker_roll == -2:
                damage *= mult
                if target_roll == -1:
                    damage *= mult
                    if verbose:
                        print(utils.colorize(f"Critical Hit, while off guard! {mult*mult}x damage", ['bold', 'red', 'on_black']))
                
                elif target_roll == -2:
                    damage /= mult
                    if verbose:
                        print(utils.colorize("Critical Hit and Block! 1x damage", ['bold', 'red', 'on_black']))
                else:
                    if verbose:
                        print(utils.colorize(f"Critical Hit! {mult}x damage", ['bold', 'red', 'on_black']))

            elif attacker_roll == -1:
                if target_roll == -2 and not range_weapon:
                    self_damage = target.stats[PlayerStat.attack]//mult
                    self.attr[PlayerStat.health] = max(0, self.attr[PlayerStat.health] - self_damage)
                    if verbose:
                        print(f'{target.name} Critically Reversed {self.name}\'s attack! {self.name} lost {utils.colorize(f"{self_damage} HP", PlayerStat.health.color().value)}')
                else:
                    damage = 0
                    if verbose:
                        print(utils.colorize('Attacker Epic Miss! No Damage!', ['bold', 'red', 'on_black']))

            target.attr[PlayerStat.health] = max(0, target.attr[PlayerStat.health] - damage) # Apply damage 
            sta_degredation = min(0, effects.get(PlayerStat.stamina, 0))
            self.attr[PlayerStat.stamina] = max(0, sta_degredation + self.attr[PlayerStat.stamina]) # reduce player stamina
            if verbose:
                if effects.get(PlayerStat.attack, 0) == 0:
                    print(f"{self.name} [{utils.colorize(str(target.attr[PlayerStat.stamina])+' STA', StatColor.stamina.value)}] Lost {utils.colorize(str(sta_degredation)+' STA', StatColor.stamina.value)} attacking {target.name} [{utils.colorize(str(target.attr[PlayerStat.health])+' HP', StatColor.health.value)}] for {utils.colorize( str(damage)+' ATK', StatColor.attack.value)}!") # Print attack message
                else:
                    print(f"{self.name} [{utils.colorize(str(target.attr[PlayerStat.stamina])+' STA', StatColor.stamina.value)}] Lost {utils.colorize(str(sta_degredation)+' STA', StatColor.stamina.value)} attacking {target.name} [{utils.colorize(str(target.attr[PlayerStat.health])+' HP', StatColor.health.value)}] for {utils.colorize( str(damage)+' ATK', StatColor.attack.value)} with a \033[1m\033[4m{'Ranged Weapon' if range_weapon else 'Melee Weapon'}\033[0m!") # Print attack message
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
                damage -= player.stats[PlayerStat.defense] # Reduce damage based on target's defense 
                damage = max(5, damage) # Make sure damage is at least 1

                if attacker_role == -2:
                    damage *= 2
                    if verbose:
                        print("Critical hit!")
                elif attacker_role == -1:
                    damage = 0
                    if verbose:
                        print(f'{player} missed their spell!')

                if target_role == -2:
                    damage == 0
                    if verbose:
                        print("Attack Dodged!")
                elif target_role == -1:
                    damage *= 2
                    if verbose:
                        print('Enemy caught off guard!')

                player.attr[PlayerStat.health] = max(0, player.attr[PlayerStat.health] - damage) # Apply damage
                self.attr[PlayerStat.mana] = max(0,self.attr[PlayerStat.mana] + effects.get(PlayerStat.mana, 0)) # reduce player stamina
                if verbose:
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
                
                if verbose:
                    print(res+']')
            
            return 0
        else:
            if verbose:
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
        if verbose:
            print(res)

    def use(self, item, target: 'Player'=None, use_armor=True):
        effects = item.use()
        if item.type == ItemType.potion:
            self.use_item(effects, target)

        elif item.type == ItemType.magic:
            self.use_magic(effects, target)

        elif item.type in [ItemType.melee, ItemType.ranged]:
            return self.use_attack(effects, item.type, target, use_armor=use_armor)
        
        if item.uses == 0 and item in self.items[item.type]:
            self.items[item.type].remove(item)
        self.sort_inv()
        return effects

    def give(self, item: item.Item, target: 'Player'):
        temp = item
        self.items[item.type].remove(item)
        target.items[item.type].append(temp)
        target.sort_inv()
        if verbose:
            print(f'{self.name} gave {target.name} - {utils.colorize(item.type.name, ["bold", "cyan", "on_black"])}')

    def sort_inv(self):
        for item_list in self.items.values():
            item_list.sort(key=lambda x: (x.rank, next(iter(x.effects.values()))), reverse=True)
        return self

    def get_inputs(self):
        return [val for val in self.stats.values()] + [val for key, val in self.attr.items() if key != 'name']

    def asdict(self):
        return {'name': self.name, 'stats': self.stats, 'attr': self.attr, 'items': self.items, 'usable_items': self.usable_items, 'rank': self.rank, 'id': self.id}

    @classmethod
    def get(cls, character_id : str):
        try:
            character_ref = db.collection('characters')
            character = character_ref.document(character_id).get()
            if character.exists:
                character_df = character.asdict()
                character_result = cls(**character_df)
                character_result.character_id = character_id
                return character_result, 200
            return character_result, 404
        except:
            return character_result, 500
    
    def update(self, update_fields):
        character_df = self.asdict()
        for key, value in update_fields.keys():
            character_df[key] = value
        character_ref = db.collection("characters").document(self.character_id)
        character_ref.update(update_fields)
        return True
    
    @staticmethod
    def delete(character_id):
        try:
            character_ref = db.collection("characters").document(character_id).delete()
            return True, 200
        except:
            return False, 404

    @classmethod
    def create(cls, character_df):
        # TODO create function; input character_df; turn into class and add to db server; return Character new_character
        result = cls(**character_df)
        character_ref = db.collection("characters")
        character_ref.document(result.character_id).set(result.asdict())
        return result, 200

    def purchaseItem(self, item_idx):
        cur_item = item.get(item_idx)
        if cur_item.priceGems < self.num_gems and cur_item.priceCrystals < self.num_crystals and cur_item.priceDiamonds < self.num_diamonds and self.inventory.storeItem(item_idx):
            self.num_gems -= cur_item.priceGems
            self.num_crystals -= cur_item.priceCrystals
            self.num_diamonds -= cur_item.priceDiamonds
            return True
        return False


def generate_player(name, level=None):
    attr = {
        PlayerStat.level: level if level else random.randint(25,100),
        PlayerStat.health: 100,
        PlayerStat.mana: 100,
        PlayerStat.stamina: 100,
        'name': name,
    }

    stats = {
        PlayerStat.attack: 0,
        PlayerStat.defense: 0,
        PlayerStat.charisma: 0,
        PlayerStat.intelligence: 0,
        PlayerStat.wisdom: 0
    }

    for i in range(2*attr[PlayerStat.level]):
        choice = random.choice(list(stats.keys()))
        if stats[choice] < 50:
            stats[choice] += 1
        else:
            i -= 1

    items = item.generate_items(random.randint(14,18), attr[PlayerStat.level])
    return Player(stats=stats, attr=attr, items=items).sort_inv()