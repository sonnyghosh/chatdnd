import random
from . import party, g_vars
ItemType = g_vars.ItemType
PlayerStat = g_vars.PlayerStat
import os
import time
from game.gametests import utils

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

class Battle:
    def __init__(self, player_party, enemy_party):
        self.player_party = player_party
        self.enemy_party = enemy_party
    
    def validate(self):
        assert self.player_party.validate_party() # player party memebers invalid
        assert self.enemy_party.validate_party() # enemy party memebers invalid

    def play_turn(self, mode='enemy', debug=False, auto_play=False):
        if debug:
            print('Debug mode:', debug)
        if mode == 'enemy':
            print('Enemy Turn:')
        if mode not in ['enemy', 'auto', 'player']:
            print(f'Not a valit mode: [{mode}]')

        toggle = self.enemy_party if mode == 'enemy' else self.player_party
        op_toggle = self.player_party if mode == 'enemy' else self.enemy_party

        assert toggle == self.player_party if mode != 'enemy' else toggle == self.enemy_party

        st = {
            PlayerStat.attack: 0,
            PlayerStat.defense: 0,
            PlayerStat.charisma: 0,
            PlayerStat.intelligence: 0,
            PlayerStat.wisdom: 0,
            PlayerStat.stamina: 0,
            PlayerStat.mana: 0,
            PlayerStat.health: 0,
            'item': 0,
            'weapon': 0,
            'magic': 0,
        }
        cur_party = toggle.get_alive_players()
        for player in cur_party:
            use_log = {}
            op_party = op_toggle.get_alive_players()
            if len(op_party) < 1: break

            if debug and mode=='player':
                print(utils.colorize('Using Default Attack', 'red'))
                print(utils.colorize('', ''))
                use_log = player.attack(random.choice(op_party))
                break

            # determine action to take 
            if mode == 'player':
                # print out all of the players that are still alive
                print(op_toggle.get_party_members_names())
                print(toggle.get_party_members_names())

                # prompt user to make a move
                prompt = f'{player.name}\'s turn!\nHere is {player.name}\'s redout:\n{player}\n - To attack type "attack"\n - To use an item type "use (Item type #)"\n - To regen HP, MP, and STA type "pass"\nAction: '
                action = prompt_user(prompt=prompt, invalid=lambda x: x not in ['attack', 'pass'] and len(x.split()) < 2)
            
            # random action for bot
            else:
                action = random.choices(['attack', 'use', 'pass'], weights=[0.33, 0.33, 0.33])[0]
                print(utils.colorize(f'{toggle.name}', 'red' if mode == 'enemy' else 'cyan'), utils.colorize(f'Team making action:', 'green'), utils.colorize(f'{action}', 'white'))

            # Action - Pass: regens HP, MP, STA
            if (mode == 'player' and action == 'pass') or (mode != 'player' and (player.attr[PlayerStat.mana] < 30 or player.attr[PlayerStat.stamina] < 30)):
                stamina_gain = int(player.attr[PlayerStat.level]/10) + random.randint(0,5)
                mana_gain = int(player.attr[PlayerStat.level]/10) + random.randint(0,5)
                health_gain = int(player.attr[PlayerStat.level]/10) + random.randint(0,5)
                player.attr[PlayerStat.mana] = min(100, player.attr[PlayerStat.mana] + stamina_gain)
                player.attr[PlayerStat.stamina] = min(100, player.attr[PlayerStat.stamina] + mana_gain)
                player.attr[PlayerStat.health] = min(100, player.attr[PlayerStat.health] + health_gain)
                if mode == 'player':
                    clr_t()
                st = agg(st, {PlayerStat.stamina : stamina_gain, PlayerStat.health : health_gain, PlayerStat.mana: mana_gain})
                print(f'{player.name} has rested and gained {health_gain} HP, {mana_gain} MP and {stamina_gain} STA.')

            # Action - Use Attack
            elif (mode == 'player' and action == 'attack') or (mode != 'player' and random.random() > 0.3):
                weapon_choice = player.get_item_type(ItemType.weapon)
                # choosing a weapon from 'weapon_choice'
                if mode != 'player':
                    target = random.choice(op_party)
                    if random.random() > 0.1 and len(weapon_choice) > 0:
                        weapon = random.choice(range(len(weapon_choice)))
                    else:
                        weapon = -1
                else:
                    prompt = op_toggle.get_party_members_names() + '\nWho would you like to attack? Enter the number of the character: '
                    target_idx = prompt_user(prompt=prompt, invalid=lambda x: x not in range(len(op_party)), fn=lambda x: int(x))
                    target = op_party[target_idx]
                    prompt = f'{player.get_weapons_str(spacer="")}-1. Fist - use base attack stat [ {player.stats["ATK"]} ATK ]\nPlease Select a weapon to use: '
                    weapon = prompt_user(prompt=prompt, invalid=lambda x: x not in range(-1,len(weapon_choice)), fn=lambda x: int(x))
                    if not debug:
                        clr_t()
                # Decide to use armor 
                if mode == 'enemy' and not auto_play:
                    ans = prompt_user(f'{target.name} is being attacked... Use armor for extra DEF? [Y]/[N]', invalid=lambda x: x in ['Y','N'], fn=lambda x: str.upper(x.split()[0]))
                    use_armor = True if ans == 'Y' else False
                else:
                    use_armor = True
                # Use weapon attack
                if weapon >= 0:
                    weapon = weapon_choice[weapon]
                    use_log = player.use(weapon, target, use_armor=use_armor)
                # Use fist attack
                else:
                    use_log = player.attack(target, use_armor=use_armor)
            
            # Action - Use an Item
            elif mode != 'player' or (mode == 'player' and action.startswith('use')):

                # TODO: Make intelligent method of selecting moves
                # Random item to use for the bot
                if mode != 'player':
                    target = random.choice(op_party)
                    possible = []
                    tries = 0
                    while len(possible) == 0:
                        possible = player.get_item_type(ItemType(random.choices([0, 1], weights=[0.35,0.65])[0]))
                        tries += 1
                        if tries > 20: break

                    if len(possible) == 0:
                        print('No items to use:')
                        use_log = player.attack(target)
                        continue
                    item = random.choice(possible)
                # player Picks Item to use
                else:
                    print(action)
                    spacer = '\n\t'
                    item_list = player.items[ItemType(int(action.split()[1]))] 
                    prompt = f'{player.name}\'s Current Items:{spacer}{"".join([str(i)+". "+str(x)+ spacer for i, x in enumerate(item_list)])}\nPlease enter the item that you want to use: '
                    item_ind = prompt_user(prompt=prompt, invalid=lambda x: x not in range(len(item_list)), fn=lambda x: int(x))
                    item = item_list[item_ind]

                # Use potion or util magic
                if item.type == 0 or PlayerStat.attack not in item.effects.keys():
                    st = agg(st, {'item': 1})
                    # Bot chooses who to use it on
                    if mode != 'player':
                        if random.random() > 0.5:
                            use_log = player.use(item) # use on self
                        else:
                            use_log = player.use(item, random.choice(cur_party)) # use on party
                    
                    # Player chooses who to use it on
                    else:
                        prompt = 'Who would you like to use it on? [S]elf, [F]riend: '
                        target_idx = prompt_user(prompt=prompt, invalid=lambda x: x not in ['S','F'], fn=lambda x: str.upper(x.split()[0]))
                        
                        # Use item on self
                        if target_idx == 'S':
                            clr_t()
                            use_log = player.use(item)
                        
                        # Use on party member
                        else:
                            targets = self.player_party.get_party_members_names()
                            prompt = f'{targets}\nWho would you like to use {item.name} on? Enter the number of the character: '

                            if len(targets) > 1:
                                target_idx = prompt_user(prompt=prompt, invalid=lambda x: x not in range(len(cur_party)), fn=lambda x: int(x))
                            else:
                                target_idx = 0
                            clr_t()
                            use_log = player.use(item, cur_party[target_idx])
               
                # Use magic attack
                elif item.type == 1:
                    st = agg(st, {'magic': 1})
                    # Player chooses who to attack
                    if mode == 'player':
                        targets = op_toggle.get_party_members_names()
                        prompt = f'{targets}\nWho would you like to use {item.name} on? Enter the number of the character: '
                        if len(targets) > 1:
                            target_idx = prompt_user(prompt=prompt, invalid=lambda x: x not in range(len(op_party)), fn=lambda x: int(x))                       
                        else:
                            target_idx = 0
                        clr_t()
                        use_log = player.use(item, op_party[target_idx])
                    # Bot randomly choses opponet
                    else:
                        use_log = player.use(item, random.choice(op_party))    
            
            # Action - Give item to teammate

            st = agg(st, use_log)

        return st

    def combat_round(self, debug=False, auto_play=False):
        # Player turn
        self.validate()
        if auto_play:
            p_stats = self.play_turn(mode='auto', debug=debug, auto_play=auto_play)
        else:
            p_stats = self.play_turn(mode='player')
        p_stats['moves'] = p_stats.get('moves',0) + len(self.player_party.get_alive_players())
        p_stats['turns'] = p_stats.get('turns',0) + 1
        # Enemy turn 
        self.validate()
        e_stats = self.play_turn(mode='enemy', debug=debug)
        e_stats['moves'] = e_stats.get('moves',0)  + len(self.enemy_party.get_alive_players())
        e_stats['turns'] = e_stats.get('turns',0) + 1
        return p_stats, e_stats
    
    def start_game(self, debug=False, auto_play=False, readable=False):
        ts  = 0.00001 if not readable else 0.9
        p_stats = {}
        e_stats = {}
        if not (debug or auto_play):
            input('Press any key to begin the battle!')
            clr_t()

        while (self.player_party.get_alive_players() and self.enemy_party.get_alive_players()):
            a,b = self.combat_round(debug=debug, auto_play=auto_play)
            p_stats = agg(p_stats, a)
            e_stats = agg(e_stats, b)
            if readable and debug:
                time.sleep(ts)
        
        p_stats = agg(p_stats, {'Wins': 1} if self.player_party.get_alive_players() else {'Losses': 1})
        e_stats = agg(e_stats, {'Wins': 1} if self.enemy_party.get_alive_players() else {'Losses': 1})
        
        if not debug and auto_play:
            clr_t()
            print("Combat over!")
            if len(self.player_party.get_alive_players()) > 0:
                print('You won, Congratulations!')
            else:
                print('You Lose, Weep in pain!')
        if not auto_play:
            return {'Player':p_stats, 'Enemy': e_stats}
        else:
            return p_stats, e_stats
        