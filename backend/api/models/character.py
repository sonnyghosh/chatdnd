from dataclasses import dataclass, field, asdict

from inventory import Inventory
from item import Item
from utils import generate_id, db
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
    
    @classmethod
    def get(cls, character_id : str):
        try:
            character_ref = db.collection('characters')
            character = character_ref.document(character_id).get()
            if character.exists:
                character_df = character.to_dict()
                character_result = cls(character_df["character_name"], character_df["hp"], character_df["mp"], character["stamina"], character_df["game_class"], character_df["isPartyLeader"],
                                       character_df["inventory_id"], character_df["num_gems"], character_df["num_crystals"], character_df['num_diamonds'], character_df['attack'], character_df['defense'],
                                       character_df['intelligence'], character_df['wisdom'], character_df['charisma'])
                character_result.character_id = character_id
                return character_result, 200
            return character_result, 404
        except:
            return character_result, 500
    
    def update(self, update_fields):
        character_df = asdict(self)
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
        character_ref.document(result.character_id).set(asdict(result))
        return result, 200