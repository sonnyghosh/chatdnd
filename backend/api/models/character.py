from dataclasses import dataclass

from inventory import Inventory
from item import Item
@dataclass
class Character:
    id : int
    character_name : str
    hp : int
    mp : int
    stamina : int
    game_class : str
    isPartyLeader : bool
    inventory : Inventory
    numGems : int
    numCrystals : int
    numDiamonds : int
    attack : int
    defense : int
    intelligence : int
    wisdom : int
    charisma : int 

    def purchaseItem(self, item_idx):
        cur_item = Item.get(item_idx)
        item_price = (cur_item.numGems, cur_item.numCrystals, cur_item.numDiamonds)
        if cur_item.numGems < self.numGems and item_crystals < self.numCrystals and item_diamonds < self.numDiamonds and self.inventory.storeItem(item_idx):
            self.numGems -= item_gems
            self.numCrystals -= item_crystals
            self.numDiamonds -= item_diamonds
            return True
        return False
    
    def sellItem(self, item_idx):
        cur_item = Item.get(item_idx)
        item_price = (cur_item.numGems, cur_item.numCrystals, cur_item.numDiamonds)
        self.numGems += cur_item.numGems
        self.numCrystals += cur_item.numCrystals
        self.numDiamonds += cur_item.numDiamonds
        return self.inventory.dropItem(item_idx)