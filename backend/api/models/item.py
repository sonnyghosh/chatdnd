from dataclasses import dataclass

@dataclass
class Item:
    item_id : int
    name : str
    price : float
    re_sell_modifier : float
    minimum_price : float
    weight : float
    
    @classmethod
    def get(cls, item_id):
       # TODO - item = some_server.get(item_id)
       # TODO - result = cls(some_results)
       return result