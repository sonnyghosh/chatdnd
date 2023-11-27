

class Party:
    def __init__(self, members, name):
        self.name = name
        self.players = members
    
    def __str__(self) -> str:
        res = f'-------| {self.name} |-------\n\n'
        for pl in self.players:
            res += str(pl) + '\n\n'
        return res

    def get_alive_players(self):
        return [p for p in self.players if p.attr["HP"] > 0]