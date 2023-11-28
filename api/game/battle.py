import random
import party
import os

def clr_t():
    os.system('cls' if os.name == 'nt' else 'clear')

class Battle:
    def __init__(self, player_party, enemy_party):
        self.player_party = player_party
        self.enemy_party = enemy_party
        
    def combat_round(self):
        # Player turn
        cur_player_party = self.player_party.get_alive_players()
        for player in cur_player_party:
            cur_enemy_party = self.enemy_party.get_alive_players()
            print(self.enemy_party.get_party_members_names())
            print(self.player_party.get_party_members_names())

            if len(cur_enemy_party) < 1:
                break
            prompt = f'{player.name}\'s turn!\nHere is {player.name}\'s redout:\n{player}\nTo attack type "attack"\nTo use an item type "use " and the number of the item\n'
            action = ''
            while action != 'attack' and len(action.split()) < 2:
                    action = input(prompt)
            if action == "attack":
                prompt = 'Who would you like to attack? Enter the number of the character...\n'
                targets = self.enemy_party.get_party_members_names()
                target_idx = int(input(prompt + targets + str(player)))
                target = cur_enemy_party[target_idx]
                player.attack(target)
                
            elif action.startswith("use"):
                item = player.items[int(action.split()[1])]
                if item.cat != 2:
                    prompt = 'Who would you like to use it on? [S]elf, [F]riend, [E]nemy: '
                    target_idx = str.upper(input(prompt).split()[0])
                    while target_idx not in ['S','F','E']:
                        target_idx = str.upper(input(prompt).split()[0])
                else:
                    target_idx = 'E'
                clr_t()
                if target_idx == 'S':
                    player.use(item)

                elif target_idx == 'F':
                    prompt = f'Who would you like to use {item.name} on? Enter the number of the character...\n'
                    targets = self.player_party.get_party_members_names()

                    if len(targets) > 1:
                        target_idx = int(input(prompt + targets))
                        while target_idx not in range(len(self.player_party)):
                            target_idx = int(input(prompt + targets))
                        clr_t()
                    else:
                        target_idx = 0

                    if len(self.player_party) > target_idx >= 0:
                        player.use(item, cur_player_party[target_idx])

                elif target_idx == 'E':
                    prompt = f'Who would you like to use {item.name} on? Enter the number of the character...\n'
                    targets = self.enemy_party.get_party_members_names()

                    if len(targets) > 1:
                        target_idx = int(input(prompt + targets))
                        while target_idx not in range(len(self.enemy_party)):
                            target_idx = int(input(prompt + targets))
                        clr_t()
                    else:
                        target_idx = 0

                    if len(self.enemy_party) > target_idx >= 0:
                        player.use(item, cur_enemy_party[target_idx])
                else:
                    print('that was not a valid action')
        clr_t()
        # Enemy turn   
        cur_enemy_party = self.enemy_party.get_alive_players()
        for enemy in cur_enemy_party:
            cur_player_party = self.player_party.get_alive_players()
            target = random.choice(cur_player_party)

            if random.random() > 0.6:
                enemy.attack(target)
            # TODO: Make intelligent method of selecting moves
            else:
                item = random.choice(enemy.items)
                if item.cat == 0:
                    if random.random() > 0.5:
                        enemy.use(item)
                    else:
                        enemy.use(item, random.choice(cur_enemy_party))
                
                elif item.cat == 1:
                    if 'ATK' in item.effects.keys():
                        enemy.use(item, target)
                    else:
                        if random.random() > 0.5:
                            enemy.use(item)
                        else:
                            enemy.use(item, random.choice(cur_enemy_party))
                else:
                    enemy.use(item, target)
        

    def start(self):
        while (self.player_party.get_alive_players() 
               and self.enemy_party.get_alive_players()):
            self.combat_round()

        clr_t()
        print("Combat over!")
        if len(self.player_party.get_alive_players()) > 0:
            print('You won, Congratulations!')
        else:
            print('You Lose, Weep in pain!')