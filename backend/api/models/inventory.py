from dataclasses import dataclass, field

from item import Item
from character import Character
from utils import generate_id
from . import db

@dataclass
class Inventory:
    inventory_id : str = field(init = False, default_factory=generate_id)
    weight_limit : float
    current_weight : float
    num_items : int
    item_ids : list[str] = field(default_factory=list)
    owner : Character

    def storeItem(self, item_idx):
        item, _ = Item.get(item_idx)
        new_weight = self.current_weight + item.weight
        if new_weight < self.weight_limit:
            self.item_ids.append(item_idx)
            self.current_weight = new_weight
            self.num_items += 1
            update_inventory_field = {
                'item_ids' : self.item_ids,
                'current_weight' : self.current_weight,
                'num_items' : self.num_items
            }
            self.update(update_inventory_field)
            return True
        return False
    
    def dropItem(self, item_idx):
        item, _ = Item.get(item_idx)
        if item_idx in self.item_ids:
            self.num_items -= 1
            self.current_weight -= item.weight
            self.item_ids.remove(item_idx)
            update_fields = {
                'item_ids' : self.item_ids,
                'current_weight' : self.current_weight,
                'num_items' : self.num_items
            }
            self.update(update_fields)
            return True
        return False
    
    def update(self, update_fields):
        try:
            inventory_ref = db.collection("inventory").document(self.inventory_id)
            inventory_ref.update(update_fields)
            return True, 200
        except:
            return False, 404