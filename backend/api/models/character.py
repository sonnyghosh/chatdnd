from dataclasses import dataclass
from inventory import Inventory

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
        # TODO cur_item = get(item_idx)
        # TODO item_price = (item_idx.numGems, item_idx.numCrystals, item_idx.numDiamonds)
        (item_gems, item_crystals, item_diamonds) = item_price
        if item_gems < self.numGems and item_crystals < self.numCrystals and item_diamonds < self.numDiamonds:
            self.numGems -= item_gems
            self.numCrystals -= item_crystals
            self.numDiamonds -= item_diamonds
            self.inventory.storeItem(item_idx)
        return False
    
    def sellItem(self, item_idx):
        # TODO cur_item = get(item_idx)
        # TODO item_price = (item_idx.numGems, item_idx.numCrystals, item_idx.numDiamonds)
        self.numGems += item_gems
        self.numCrystals += item_crystals
        self.numDiamonds += item_diamonds
        return self.inventory.dropItem(item_idx)