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
        return f'{self.name} - Type: {self.cat} Uses: {self.uses}, Effects | {"".join([f"{key}: {val} " for key, val in self.effects.items()])}|'

    def validate_effects(self, effects):
        """
        Validates that the keys in the effects dictionary have specific values.

        Parameters:
        - effects (dict): A dictionary representing the effects of the item on game stats.

        Returns:
        - bool: True if all keys have valid values, False otherwise.
        """
        # Define valid ranges for each stat
        valid_ranges = {
            'ATK': range(0, 31),
            'DEF': range(0, 31),
            'CHA': range(0, 31),
            'INT': range(0, 31),
            'WIS': range(0, 31),
            'HP': range(0,101),
            'LVL': range(0,5),
            'STA': range(0,101),
        }

        # Check if all keys have valid values
        for key, value in effects.items():
            if key in valid_ranges and value not in valid_ranges[key]:
                print(f"Invalid value {value} for {key}. Valid range: {valid_ranges[key]}.")
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
        elif self.uses == -1:
            return self.effects
        else:
            # If uses are already 0, the item is broken
            print(f"{self.name} is broken and cannot be used.")
            return {}

# Example usage:
# health_potion = GameItem("Health Potion", 3, {'health': 20})
# result = health_potion.use()
# print(result)
