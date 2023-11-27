import random

class Battle:
    def __init__(self, player_party, enemy_party):
        self.player_party = player_party
        self.enemy_party = enemy_party
        
    def combat_round(self):
        # Player turn
        for player in self.player_party.get_alive_players():
            prompt = f'{player.name}\'s turn!\nHere is {player.name}\'s redout:\n{player}\nTo attack type attack\nTo use an item type "use " and the number of the item\n'
            action = input(prompt)
            if action == "attack":
                target = random.choice(self.enemy_party.get_alive_players()) 
                player.attack(target)
                
            elif action.startswith("use"):
                item = player.items[int(action.split()[1])]
                target = random.choice(self.enemy_party.get_alive_players())
                player.use_item(item, target)
                
        # Enemy turn   
        for enemy in self.enemy_party.get_alive_players():
            target = random.choice(self.player_party.get_alive_players())
            enemy.attack(target)
            
    def start(self):
        while (self.player_party.get_alive_players() 
               and self.enemy_party.get_alive_players()):
            self.combat_round()
            
        print("Combat over!")