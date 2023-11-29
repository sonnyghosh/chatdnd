import random
from . import party
import os
import time

def clr_t():
    os.system('cls' if os.name == 'nt' else 'clear')

def agg(store, sample):
    store.update({key: store.get(key, 0) + val for key, val in sample.items()})
    return store

def prompt_user(prompt, invalid=lambda x : x=='attack', fn=lambda x: x):
    res = ''
    while invalid(res):
        res = fn(input(prompt))
    return res

def validate_game(party_a, party_b):
    assert party_a.validate_party() # player party memebers invalid
    assert party_b.validate_party() # enemy party memebers invalid

class Battle:
    def __init__(self, player_party, enemy_party):
        self.player_party = player_party
        self.enemy_party = enemy_party
        
    def player_turn(self):
        cur_player_party = self.player_party.get_alive_players()
        for player in cur_player_party:
            # get the current enemy players and exit if there are none left - player wins
            cur_enemy_party = self.enemy_party.get_alive_players()
            if len(cur_enemy_party) < 1: break

            # print out all of the players that are still alive
            print(self.enemy_party.get_party_members_names())
            print(self.player_party.get_party_members_names())

            # prompt user to make a move
            prompt = f'{player.name}\'s turn!\nHere is {player.name}\'s redout:\n{player}\n - To attack type "attack"\n - To use an item type "use (Item type #)"\n - To regen HP, MP, and STA type "pass"\nAction: '
            action = prompt_user(prompt=prompt, invalid=lambda x: x not in ['attack', 'pass'] and len(x.split()) < 2)

            # MOVE - Attack 
            if action == "attack":
                prompt = self.enemy_party.get_party_members_names() + '\nWho would you like to attack? Enter the number of the character: '
                target_idx = prompt_user(prompt=prompt, invalid=lambda x: x not in range(len(cur_enemy_party)), fn=lambda x: int(x))
                target = cur_enemy_party[target_idx]
                prompt = f'{player.get_weapons_str(spacer="")}-1. Fist - use base attack stat [ {player.stats["ATK"]} ATK ]\nPlease Select a weapon to use: '
                weapon_choice = player.get_weapons()
                weapon = prompt_user(prompt=prompt, invalid=lambda x: x not in range(-1,len(cur_enemy_party)), fn=lambda x: int(x))
                if weapon >= 0:
                    weapon = weapon_choice[weapon]
                    clr_t()
                    player.use(weapon, target)
                else:
                    clr_t()
                    player.attack(target)
            
            # MOVE - Use Item
            elif action.startswith("use"):
                print(action)
                spacer = '\n\t'
                item_list = player.items[int(action.split()[1])] 
                prompt = f'{player.name}\'s Current Items:{spacer}{"".join([str(i)+". "+str(x)+ spacer for i, x in enumerate(item_list)])}\nPlease enter the item that you want to use: '
                item_ind = prompt_user(prompt=prompt, invalid=lambda x: x not in range(len(item_list)), fn=lambda x: int(x))
                item = item_list[item_ind]

                # is the item utility or attack
                if item.cat == 0 or 'ATK' not in item.effects.keys():
                    prompt = 'Who would you like to use it on? [S]elf, [F]riend: '
                    target_idx = prompt_user(prompt=prompt, invalid=lambda x: x not in ['S','F'], fn=lambda x: str.upper(x.split()[0]))
                else:
                    target_idx = 'E'
                
                # use item on self
                if target_idx == 'S':
                    clr_t()
                    player.use(item)
                
                # use item on a friend
                elif target_idx == 'F':
                    targets = self.player_party.get_party_members_names()
                    prompt = f'{targets}\nWho would you like to use {item.name} on? Enter the number of the character: '

                    if len(targets) > 1:
                        target_idx = prompt_user(prompt=prompt, invalid=lambda x: x not in range(len(self.player_party)), fn=lambda x: int(x))
                    else:
                        target_idx = 0
                    clr_t()
                    player.use(item, cur_player_party[target_idx])
                
                # use item on enemy
                elif target_idx == 'E':
                    targets = self.enemy_party.get_party_members_names()
                    prompt = f'{targets}\nWho would you like to use {item.name} on? Enter the number of the character: '
                    if len(targets) > 1:
                        target_idx = prompt_user(prompt=prompt, invalid=lambda x: x not in range(len(self.enemy_party)), fn=lambda x: int(x))                       
                    else:
                        target_idx = 0
                    clr_t()
                    player.use(item, cur_enemy_party[target_idx])
                
                else:
                    print('that was not a valid action')

            # MOVE - Pass - action lets you regen stamina mana and health passively
            elif action == "pass":
                stamina_gain = player.attr['LVL']/10 + random.randint(0,5)
                mana_gain = player.attr['LVL']/10 + random.randint(0,5)
                health_gain = player.attr['LVL']/10 + random.randint(0,5)
                player.attr['MP'] = min(100, player.attr['MP'] + stamina_gain)
                player.attr['STA'] = min(100, player.attr['STA'] + mana_gain)
                player.attr['HP'] = min(100, player.attr['HP'] + health_gain)
                clr_t()
                print(f'{player.name} has rested and gained {health_gain} HP, {mana_gain} MP and {stamina_gain} STA.')

        clr_t()

    def auto_turn(self, mode='Enemy'):
        toggle = self.enemy_party if mode == 'Enemy' else self.player_party
        op_toggle = self.player_party if mode == 'Enemy' else self.enemy_party
        st = {
            'ATK': 0,
            'DEF': 0,
            'CHA': 0,
            'INT': 0,
            'WIS': 0,
            'STA': 0,
            'MP': 0,
            'HP': 0,
            'item': 0,
            'weapon': 0,
            'magic': 0,
        }
        cur_party = toggle.get_alive_players()
        for player in cur_party:

            op_party = op_toggle.get_alive_players()
            if len(op_party) < 1: break
            target = random.choice(op_party)

            # choose to pass
            if player.attr['MP'] < 30 or player.attr['STA'] < 30:
                stamina_gain = random.randint(10,20)
                mana_gain = random.randint(10,20)
                health_gain = random.randint(10,20)
                player.attr['MP'] = min(100, player.attr['MP'] + stamina_gain)
                player.attr['STA'] = min(100, player.attr['STA'] + mana_gain)
                player.attr['HP'] = min(100, player.attr['HP'] + health_gain)
                st = agg(st, {'STA' : stamina_gain, 'HP' : health_gain, 'MP': mana_gain})
                print(f'{player.name} has rested and gained {health_gain} HP, {mana_gain} MP and {stamina_gain} STA.')

            # fist attack
            elif random.random() > 0.9:
                dmg, sta = player.attack(target)
                st = agg(st, {'ATK':dmg, 'STA':sta})
            # TODO: Make intelligent method of selecting moves

            # random item use 10% potion 20% magic 70% weapon
            else:
                possible = []
                tries = 0
                while len(possible) == 0:
                    possible = player.get_item_ind(random.choices([0, 1, 2], weights=[0.1,0.2,0.7])[0])
                    tries += 1
                    if tries > 20: break

                if len(possible) == 0:
                    print('No items to use:')
                    dmg, sta = player.attack(target)
                    st = agg(st, {'ATK':dmg, 'STA':sta})
                    continue
                item = random.choice(possible)

                # use potion
                if item.cat == 0:
                    st = agg(st, {'item': 1})
                    if random.random() > 0.5:
                        use_log = player.use(item) # use on self
                    else:
                        use_log = player.use(item, random.choice(cur_party)) # use on party
                
                # use magic
                elif item.cat == 1:
                    st = agg(st, {'magic': 1})
                    if 'ATK' in item.effects.keys():
                        use_log = player.use(item, target)
                    else:
                        if random.random() > 0.5:
                            use_log = player.use(item)
                        else:
                            use_log = player.use(item, random.choice(cur_party))

                # use weapon
                else:
                    st = agg(st, {'weapon': 1})
                    use_log = player.use(item, target)
                
                st = agg(st, use_log)

        return st

    def combat_round(self):
        # Player turn
        self.player_turn()
        # Enemy turn   
        self.auto_turn()

    def start_auto(self, readable=False):
        ts  = 0.00001 if not readable else 0.9
        clr_t()
        p_stats = {}
        e_stats = {}
        while (self.player_party.get_alive_players() and self.enemy_party.get_alive_players()):
            validate_game(self.player_party, self.enemy_party)
            round_stats = self.auto_turn(mode='Player')
            p_stats = agg(p_stats, round_stats)
            del round_stats
            p_stats['moves'] = p_stats.get('moves',0) + len(self.player_party.get_alive_players())
            p_stats['turns'] = p_stats.get('turns',0) + 1
            time.sleep(ts)
            validate_game(self.player_party, self.enemy_party)
            round_stats = self.auto_turn()
            e_stats = agg(e_stats, round_stats)
            del round_stats
            e_stats['moves'] = e_stats.get('moves',0)  + len(self.enemy_party.get_alive_players())
            e_stats['turns'] = e_stats.get('turns',0) + 1
            time.sleep(ts)

            if e_stats['turns'] > 10000 or p_stats.get('turns',0) > 10000: break

        print("Combat over!")
        if len(self.player_party.get_alive_players()) > 0:
            print('You won, Congratulations!')
        else:
            print('You Lose, Weep in pain!')
        return p_stats, e_stats

    def start(self):
        input('Press any key to begin the battle!')
        clr_t()
        while (self.player_party.get_alive_players() and self.enemy_party.get_alive_players()):
            self.combat_round()

        clr_t()
        print("Combat over!")
        if len(self.player_party.get_alive_players()) > 0:
            print('You won, Congratulations!')
        else:
            print('You Lose, Weep in pain!')