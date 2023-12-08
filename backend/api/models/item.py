from dataclasses import dataclass, field, asdict
import json

from utils import generate_id, db

@dataclass
class Item:
    item_id : str = field(init=False, default_factory=generate_id)
    name : str
    priceCrystals : float
    priceGems : float
    priceDiamonds : float
    weight : float
    
    @classmethod
    def get(cls, item_id : str):
        try:
            items_ref = db.collection('items')
            item = items_ref.document(item_id).get()
            if item.exists:
                item_df = item.to_dict()
                item_result = cls(item_df["name"], item_df["priceCrystals"], item_df["priceGems"], item_df["priceDiamonds"], item_df["re_sell_modifier"], item["minimum_price"], item["weight"])
                item_result.id = item_id
                return item_result, 200
            return "Item not found", 404
        except:
           return "server error", 500

    @staticmethod
    def create(cls, item_df):
        result = cls(**item_df)
        item_ref = db.collection('items')
        item_ref.document(result.item_id).set(asdict(result))
        return result, 200
    
    def update(self, update_fields):
        item_df = asdict(self)
        for k, v in item_df.keys():
            item_df[k] = v
        item_ref = db.collection("items").document(self.item_id)
        item_ref.update(update_fields) 
        return self, 200