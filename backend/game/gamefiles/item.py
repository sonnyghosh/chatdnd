import random
from . import g_vars, item, hypers
PlayerStat = g_vars.PlayerStat
ItemType = g_vars.ItemType
balance_dict = g_vars.config['balance']
item_hypers, player_hypers, meta_params = hypers.load_hypers()

class Item:
    """
    Represents an item in a video game.

    Attributes:
    - name (str): The name of the item.
    - cat (int): The type of item 0-2.
    - uses (int): The number of uses the item has.
    - effects (dict): A dictionary representing the effects of the item on game stats.

    Methods:
    - use(): Applies the effects of the item and decrements its uses. If uses reach 0, the item is broken.
    """
    inf_char = '∞'

    def __init__(self, name, uses, effects):
        """
        Initializes a new Item.

        Parameters:
        - name (str): The name of the item.
        - cat (int): The type of item 0-2.
        - uses (int): The initial number of uses the item has.
        - effects (dict): A dictionary representing the effects of the item on game stats.
        """
        self.type: g_vars.ItemType = name
        self.uses: int = uses
        self.effects: dict = effects
        self.get_rank()

    def get_rank(self):
        new_rank = 0
        if self.uses != 0:
            new_rank = sum([(item_hypers.get(key, 0) + player_hypers.get(key,0)) * val for key, val in self.effects.items()]) * (min(10, abs(self.uses)) * meta_params['use_scale'])
        self.rank = max(0.1, new_rank)
        return self.rank

    def __str__(self) -> str:
        return f'{self.type.name} - Rank: {int(self.rank)}, Uses: {self.uses if self.uses != -99 else self.inf_char}, Effects [ {"".join([f"{key.value}: {val} " for key, val in self.effects.items()])}]'

    def validate_effects(self):
        """
        Validates that the keys in the effects dictionary have specific values.

        Parameters:
        - effects (dict): A dictionary representing the effects of the item on game stats.

        Returns:
        - bool: True if all keys have valid values, False otherwise.
        """
        # Define valid ranges for each stat
        valid_ranges = {
            PlayerStat.attack: range(-50, 31),
            PlayerStat.defense: range(1, 31),
            PlayerStat.charisma: range(1, 31),
            PlayerStat.intelligence: range(1, 31),
            PlayerStat.wisdom: range(1, 31),
            PlayerStat.health: range(1,101),
            PlayerStat.mana: range(-50,101),
            PlayerStat.level: range(0,2),
            PlayerStat.stamina : range(-50,101),
        }

        # Check if all keys have valid values
        for key, value in self.effects.items():
            if key in valid_ranges and value not in valid_ranges[key]:
                print(f"Invalid {key} value {value} for {self.type}. Valid range: {valid_ranges[key]}.")
                return False

        return True

    def use(self):
        """
        Applies the effects of the item and decrements its uses. If uses reach 0, the item is broken.

        Returns:
        - dict: The effects of the item on game stats.
        """
        if self.uses > 0:
            self.uses -= 1
            self.rank = self.get_rank()
            return self.effects
        elif self.uses == -99:
            return self.effects
        else:
            return {}

    def get_inputs(self):
        state = {
            PlayerStat.attack: 0,
            PlayerStat.defense: 0,
            PlayerStat.charisma: 0,
            PlayerStat.intelligence: 0,
            PlayerStat.wisdom: 0,
            PlayerStat.stamina: 0,
            PlayerStat.mana: 0,
            PlayerStat.health: 0,
        }
        for key, val in self.effects.items():
            state[key] = val
        return [val for val in state.values()] + [self.type.value]

def generate_items(n_items, level):
    bag = {
        ItemType.potion:[],   # potions
        ItemType.magic:[],   # magic
        ItemType.melee:[],   # weapon
        ItemType.ranged:[],  # ranged
        ItemType.armor:[]    # armor
    }

    for i in range(n_items):
        ind = ItemType(balance_dict['item']['item_gen'][i])
        # generate potion
        if ind == ItemType.potion:
            item_name = ind
            item_uses = random.randint(int(level/10),int(level/4))
            effect_bonus = max(2,min(30,random.randint(int(level/10),int(level/4))))
            effect_type = random.choices(g_vars.choices[item_name], weights=balance_dict['item']['potion_weights'])[0]
            item_effects = {effect_type: effect_bonus}
        
        # generate magic
        elif ind == ItemType.magic:
            item_name = ind
            item_uses = -99#random.randint(int(level/5),int(level/2))
            effect_bonus = max(2,min(30,random.randint(int(level/10),int(level/3))))
            side_effect = int(-effect_bonus * (random.random()*0.5+0.25))
            item_effects = {random.choices(g_vars.choices[item_name], weights=balance_dict['item']['magic_weights'])[0]: effect_bonus, PlayerStat.mana: side_effect}

        # generate melee
        elif ind == ItemType.melee:
            item_name = ind
            item_uses = random.randint(int(level/5),int(level/4))
            effect_bonus = max(2,min(30,random.randint(int(level/5),int(level/2.5))))
            side_effect = int(-effect_bonus * (random.random()*0.5+0.25))
            item_effects = {PlayerStat.attack: effect_bonus,PlayerStat.stamina: side_effect}

        # generate ranged
        elif ind == ItemType.ranged:
            item_name = ind
            item_uses = random.randint(int(level/5),int(level/4))
            effect_bonus = max(2,min(30,random.randint(int(level/5),int(level/2.5))))
            side_effect = int(-effect_bonus * (random.random()*0.5+0.25))
            item_effects = {PlayerStat.attack: effect_bonus,PlayerStat.stamina: side_effect}
        
        # generate armor
        elif ind == ItemType.armor:
            item_name = ind
            item_uses = 100
            effect_bonus = max(2,min(30,random.randint(int(level/10),int(level/5))))
            side_effect = int(-effect_bonus * (random.random()*0.2) - 1)
            item_effects = {PlayerStat.defense: effect_bonus, PlayerStat.stamina: side_effect}

        bag[g_vars.ItemType(ind)].append(item.Item(item_name, item_uses, item_effects))
    return bag
    
Fist = Item(ItemType.melee, -99, {PlayerStat.attack:0})
Pass = Item(ItemType.none, -99, {})
# Example usage:
# health_potion = GameItem("Health Potion", 3, {'health': 20})
# result = health_potion.use()
# print(result)