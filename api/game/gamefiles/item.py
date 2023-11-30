import random
from . import g_vars, item
PlayerStat = g_vars.PlayerStat

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
            new_rank = sum([val for val in self.effects.values()]) * (self.uses if self.uses > 1 else 2)
            if self.type == 0:
                new_rank //= 2
        self.rank = new_rank
        return new_rank

    def __str__(self) -> str:
        return f'{self.name} - Rank: {self.rank} Uses: {self.uses if self.uses != -99 else self.inf_char}, Effects [ {"".join([f"{key}: {val} " for key, val in self.effects.items()])}]'

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
                print(f"Invalid {key} value {value} for {self.name}. Valid range: {valid_ranges[key]}.")
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
            return self.effects
        elif self.uses == -99:
            return self.effects

def generate_items(n_items, level):
    bag = {
        g_vars.ItemType.potion:[],   # potions
        g_vars.ItemType.magic:[],   # magic
        g_vars.ItemType.weapon:[],   # weapon
        g_vars.ItemType.armor:[]    # armor
    }
    item_gen = [0,1,2,3,1,0,2,2,0,0,1,1,0,1,2,0,1,2] # order for items to be generated
    potion_weight = [0.05,0.15,0.1,0.1,0.1,0.25,0.125,0.125]
    magic_weight = [0.4,0.3,0.1,0.1,0.1]
    for i in range(n_items):
        ind = item_gen[i]
        # generate potion
        if ind == 0:
            item_name = g_vars.ItemType(ind)
            item_uses = random.randint(int(level/10),int(level/4))
            effect_bonus = max(2,min(30,random.randint(int(level/10),int(level/4))))
            effect_type = random.choices(g_vars.choices[item_name], weights=potion_weight)[0]
            item_effects = {effect_type: effect_bonus}
        
        # generate magic
        elif ind == 1:
            item_name = g_vars.ItemType(ind)
            item_uses = -99#random.randint(int(level/5),int(level/2))
            effect_bonus = max(2,min(30,random.randint(int(level/10),int(level/3))))
            side_effect = int(-effect_bonus * (random.random()*0.5+0.5))
            item_effects = {random.choices(g_vars.choices[item_name], weights=magic_weight)[0]: effect_bonus,PlayerStat.mana: side_effect}

        # generate weapon
        elif ind == 2:
            item_name = g_vars.ItemType(ind)
            item_uses = random.randint(int(level/5),int(level/4))
            effect_bonus = max(2,min(30,random.randint(int(level/10),int(level/3))))
            side_effect = int(-effect_bonus * (random.random()*0.5+0.5))
            item_effects = {g_vars.choices[item_name]: effect_bonus,PlayerStat.stamina: side_effect}
        
        # generate armor
        elif ind == 3:
            item_name = g_vars.ItemType(ind)
            item_uses = 100
            effect_bonus = max(2,min(30,random.randint(int(level/10),int(level/5))))
            side_effect = int(-effect_bonus * (random.random()*0.2) -1)
            item_effects = {g_vars.choices[item_name]: effect_bonus,PlayerStat.stamina: side_effect}

        bag[g_vars.ItemType(ind)].append(item.Item(item_name, item_uses, item_effects))
    return bag
    
# Example usage:
# health_potion = GameItem("Health Potion", 3, {'health': 20})
# result = health_potion.use()
# print(result)
