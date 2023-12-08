
@dataclass
class Character:
    character_id : str = field(init=False, default_factory=generate_id)
    character_name : str
    hp : int
    mp : int
    stamina : int
    game_class : str
    isPartyLeader : bool = False
    inventory_id : str
    num_gems : int
    num_crystals : int
    num_diamonds : int
    attack : int
    defense : int
    intelligence : int
    wisdom : int
    charisma : int 

    def purchaseItem(self, item_idx):
        cur_item = Item.get(item_idx)
        if cur_item.priceGems < self.num_gems and cur_item.priceCrystals < self.num_crystals and cur_item.priceDiamonds < self.num_diamonds and self.inventory.storeItem(item_idx):
            self.num_gems -= cur_item.priceGems
            self.num_crystals -= cur_item.priceCrystals
            self.num_diamonds -= cur_item.priceDiamonds
            return True
        return False
    
    