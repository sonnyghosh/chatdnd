

class Party:
    def __init__(self, members, name):
        self.name = name
        self.players = members
    
    def __str__(self) -> str:
        res = f'-------| {self.name} |-------\n\n'
        for pl in self.players:
            res += str(pl) + '\n\n'
        return res

    def __len__(self) -> int:
        return len(self.players)

    def get_alive_players(self):
        return [p for p in self.players if p.attr["HP"] > 0]
    
    def get_party_members_names(self):
        res = f'{self.name}\n'
        for idx, pl in enumerate(self.get_alive_players()):
            res += f'{idx}: {pl.name} - \t'
            res += f'|{"".join([f"{key}: {val} |" for key, val in pl.attr.items() if key != "name"])}'
            res += f'\t|{"".join([f"{key}: {val} |" for key, val in pl.stats.items()])}\n'
        return res