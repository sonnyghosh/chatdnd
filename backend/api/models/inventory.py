from dataclasses import dataclass

from item import Item
from character import Character

@dataclass
class Inventory:
    inventory_id : int
    weight_limit : float
    current_weight : float
    num_items : int
    item_ids : list
    owner : Character

    def storeItem(self, item_idx):
        item = Item.get_item(item_idx)
        new_weight = self.current_weight + item.weight
        if new_weight < self.weight_limit:
            self.item_ids.append(item_idx)
            self.current_weight = new_weight
            return True
        return False
    
    def dropItem(self, item_idx):
        if item_idx in self.item_ids:
            self.item_ids.remove(item_idx)
            return True
        return False