from dataclasses import dataclass, field, asdict
import json

from . import db
from utils import generate_id

@dataclass
class Item:
    item_id : str = field(init=False, default_factory=generate_id)
    name : str
    price : float
    re_sell_modifier : float
    minimum_price : float
    weight : float
    
    @classmethod
    def get(cls, item_id : str):
        try:
            items_ref = db.collection('items')
            item = items_ref.document(item_id).get()
            if item.exists:
                item_df = item.to_dict()
                item_result = cls(item_df["name"], item_df["price"], item_df["re_sell_modifier"], item["minimum_price"], item["weight"])
                item_result.id = item_id
                return item_result, 200
            return "Item not found", 404
        except:
           return {
               "id" : "none"
           }

    @staticmethod
    def add(item):
        item_dict = asdict(item)
        item_json = json.dump(item_dict)
        try:
            item_ref = db.collection('items')
            item_ref.document(item.item_id).set(item_json)
            return True, 200
        except:
            return False, 404