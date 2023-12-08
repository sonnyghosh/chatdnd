from class_utils import generate_id, db

class Decision:

    def __init__(self) -> None:
        self.id = generate_id()
        self.choices = []
        self.decision = ''
    
    def get_choices(self):
        return self.choices
    
    def get_decision(self):
        return self.decision
    