import random
from . import g_vars, item 

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

    def __init__(self, name, cat, uses, effects):
        """
        Initializes a new Item.

        Parameters:
        - name (str): The name of the item.
        - cat (int): The type of item 0-2.
        - uses (int): The initial number of uses the item has.
        - effects (dict): A dictionary representing the effects of the item on game stats.
        """
        self.name = name
        self.cat = cat
        self.uses = uses
        self.effects = effects

    def __str__(self) -> str:
        return f'{self.name} - Type: {self.cat} Uses: {self.uses}, Effects [ {"".join([f"{key}: {val} " for key, val in self.effects.items()])}]'

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
            'ATK': range(-50, 31),
            'DEF': range(0, 31),
            'CHA': range(0, 31),
            'INT': range(0, 31),
            'WIS': range(0, 31),
            'HP': range(0,101),
            'MP': range(-50,101),
            'LVL': range(0,2),
            'STA': range(-50,101),
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
        else:
            # If uses are already 0, the item is broken
            print(f"{self.name} is broken and cannot be used.")
            return {}

def generate_items(n_items, level):
    bag = {
        0:[],   # potions
        1:[],   # magic
        2:[],   # weapon
        3:[]    # armor
    }
    item_gen = [0,1,2,3,1,0,2,2,0,0,1,1,0,1,2,0,1,2] # order for items to be generated
    potion_weight = [0.05,0.15,0.1,0.1,0.1,0.25,0.125,0.125]
    magic_weight = [0.4,0.3,0.1,0.1,0.1]
    for i in range(n_items):
        ind = item_gen[i]
        # generate potion
        if ind == 0:
            item_name = g_vars.item_names[ind]
            item_type = ind
            item_uses = random.randint(int(level/10),int(level/4))
            effect_bonus = min(30,random.randint(int(level/20),int(level/4)))
            item_effects = {random.choices(g_vars.choices[g_vars.item_names[ind]], weights=potion_weight)[0]: effect_bonus}
        
        # generate magic
        elif ind == 1:
            item_name = g_vars.item_names[ind]
            item_type = ind
            item_uses = random.randint(int(level/5),int(level/2))
            effect_bonus = min(30,random.randint(int(level/10),int(level/3)))
            side_effect = int(-effect_bonus * (random.random()*0.5+0.5))
            item_effects = {random.choices(g_vars.choices[g_vars.item_names[ind]], weights=magic_weight)[0]: effect_bonus,'MP': side_effect}

        # generate weapon
        elif ind == 2:
            item_name = g_vars.item_names[ind]
            item_type = ind
            item_uses = random.randint(int(level/6),int(level/4))
            effect_bonus = min(30,random.randint(int(level/10),int(level/3)))
            side_effect = int(-effect_bonus * (random.random()*0.5+0.5))
            item_effects = {g_vars.choices[g_vars.item_names[ind]]: effect_bonus,'STA': side_effect}
        
        # generate armor
        elif ind == 3:
            item_name = g_vars.item_names[ind]
            item_type = ind
            item_uses = 100
            effect_bonus = min(30,random.randint(int(level/10),int(level/3)))
            side_effect = int(-effect_bonus * (random.random()*0.2) -1)
            item_effects = {g_vars.choices[g_vars.item_names[ind]]: effect_bonus,'STA': side_effect}

        bag[ind].append(item.Item(item_name, item_type, item_uses, item_effects))
    return bag
    
# Example usage:
# health_potion = GameItem("Health Potion", 3, {'health': 20})
# result = health_potion.use()
# print(result)
