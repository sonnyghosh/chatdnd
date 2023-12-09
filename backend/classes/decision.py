from dataclasses import dataclass, asdict
from class_utils import generate_id, db

@dataclass
class Decision:

    def __init__(self) -> None:
        self.id = generate_id()
        self.text : str = ''
    
    @classmethod
    def get(cls, decision_id):
        try:
            decision_ref = db.collection('decisions')
            decision = decision_ref.document(decision_id).get()
            if decision.exists:
                decision_df = decision.asdict()
                decision_result = cls(**decision_df)
                decision_result.decision_id = decision_id
                return decision_result, 200
            return decision_result, 404
        except:
            return decision_result, 500
    

    def asdict(self):
        return asdict(self)