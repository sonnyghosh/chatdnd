import random
from . import item
from backend.game.gamefiles import g_vars, hypers, AI, save_load
ItemType = g_vars.ItemType
PlayerStat = g_vars.PlayerStat
StatColor = g_vars.StatColor
import os
import time
from game.gametests import utils
save_location = utils.dataset_file
balance_dict = g_vars.config['balance']
item_hypers, player_hypers, meta_params = hypers.load_hypers()
convert = {'pass': 3, 'attack': 0, 'use': 1, 'give': 2}
verbose = g_vars.config['meta']['verbose']

model_Auto = AI.Agent(idx=6)
model_Enemy = AI.Agent(idx=6)

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

    def pass_move(self, player, mode, st):
        st = agg(st, {'pass':1})
        stamina_gain = int(player.attr[PlayerStat.level]/10) + random.randint(0,5)
        mana_gain = int(player.attr[PlayerStat.level]/10) + random.randint(0,5)
        health_gain = int(player.attr[PlayerStat.level]/10) + random.randint(0,5)
        player.attr[PlayerStat.mana] = min(100, player.attr[PlayerStat.mana] + stamina_gain)
        player.attr[PlayerStat.stamina] = min(100, player.attr[PlayerStat.stamina] + mana_gain)
        player.attr[PlayerStat.health] = min(100, player.attr[PlayerStat.health] + health_gain)
        if mode == 'player':
            clr_t()
        if verbose:
            print(f'{player.name} has rested and gained {utils.colorize("+"+str(health_gain)+" HP", "green")}, {utils.colorize("+"+str(mana_gain)+" MP", "magenta")} and {utils.colorize("+"+str(stamina_gain)+" STA", "yellow")}.')
        return {PlayerStat.stamina : stamina_gain, PlayerStat.health : health_gain, PlayerStat.mana: mana_gain}, st

    def attack_move(self, player, mode, auto_play, st, weapon, target):  
        st = agg(st, {'attack':1})         
        use_armor=True
        # Player decide to use armor 
        if mode == 'enemy':
            if not auto_play:
                ans = prompt_user(f'{target.name} is being attacked... Use armor for extra DEF? [Y]/[N]: ', invalid=lambda x: x not in ['Y','N'], fn=lambda x: str.upper(x.split()[0]))
                use_armor = True if ans == 'Y' else False

        # Use weapon attack
        if weapon.type in [ItemType.melee, ItemType.ranged] and weapon.uses > 0:
            st = agg(st, {'weapon':1})
            use_log = player.use(weapon, target, use_armor=use_armor)
        # Use fist attack
        else:
            st = agg(st, {'fist':1})      
            use_log = player.attack(target, use_armor=use_armor)
            weapon = item.Fist
        return use_log, st

    def use_move(self, player, st, thing, target):
        # Use potion or util magic
        if thing.type == ItemType.potion or PlayerStat.attack not in thing.effects.keys():
            st = agg(st, {'buff': 1})
        # Use magic attack
        elif thing.type == ItemType.magic:
            st = agg(st, {'magic': 1})
        else:
            st = agg(st, {'fist': 1, 'attack': 1})

        use_log = player.use(thing, target)
        return use_log, st

    def give_move(self, player, thing, target):
        player.give(thing, target)
        return {'give':1}

    def get_player_action(self, player, toggle, op_toggle, cur_party, op_party, debug=False):
        print(op_toggle.get_party_members_names())
        print(toggle.get_party_members_names())
        
        # prompt user to make a move
        if len(cur_party) < 2:
            addon = ''
        else:
            addon = '\n - To give an item to a party member type "give"'

        prompt = f'{player.name}\'s turn!\nHere is {player.name}\'s redout:\n{player}\n - To attack type "attack"\n - To use an item type "use (Item type #)"\n - To regen HP, MP, and STA type "pass"{addon}\nAction: '
        action = prompt_user(prompt=prompt, invalid=lambda x: x not in balance_dict['player']['human_actions'] and len(x.split()) < 2)

        if action == 'pass':
            return action, item.Pass, None
        
        elif action == 'attack':
            weapon_type = prompt_user(f'Would you like to use:\n[0] Melee Weapon\n[1] Ranged Weapon\nEnter selection: ', 
                                      invalid=lambda x: x not in [ItemType.melee, ItemType.ranged],
                                      fn=lambda x: [ItemType.melee, ItemType.ranged][int(x)])
            weapon_choice = player.get_item_type(weapon_type)

            prompt = f'{player.get_item_type_str(weapon_type, spacer="", numbered=True)}-1. Fist - use base attack stat [ {player.stats[PlayerStat.attack]} ATK ]\nPlease Select a weapon to use: '
            weapon = prompt_user(prompt=prompt, invalid=lambda x: x not in range(-1,len(weapon_choice)), fn=lambda x: int(x))
            if weapon == -1:
                weapon = item.Fist
            else:
                weapon = weapon_choice[weapon]
            
            if len(op_party) > 1:
                prompt = op_toggle.get_party_members_names() + '\nWho would you like to attack? Enter the number of the character: '
                target_idx = prompt_user(prompt=prompt, invalid=lambda x: x not in range(len(op_party)), fn=lambda x: int(x))
                target = op_party[target_idx]
            else:
                target = op_party[0]
            if not debug:
                clr_t()
            return action, weapon, target
        
        elif action == 'use':
            item_type = prompt_user('[0]: Potion\n[1]: Magic\nWhich would you like to use: ', 
                                    invalid=lambda x: type(x) is not ItemType,
                                    fn=lambda x: ItemType(int(x.strip())))
            spacer = '\n\t'
            item_list = player.items[item_type] 
            prompt = f'{player.name}\'s Current Items:{spacer}{player.get_item_type_str(item_type, numbered=True)}\nPlease enter the item that you want to use: '
            item_ind = prompt_user(prompt=prompt, invalid=lambda x: x not in range(len(item_list)), fn=lambda x: int(x))
            thing = item_list[item_ind]

            if thing.type == ItemType.potion or PlayerStat.attack not in thing.effects.keys():
                prompt = 'Who would you like to use it on? [S]elf, [F]riend: '
                target_idx = prompt_user(prompt=prompt, invalid=lambda x: x not in ['S','F'], fn=lambda x: str.upper(x.split()[0]))
                if target_idx == 'S':
                    target = player
                else:
                    targets = self.player_party.get_party_members_names()
                    prompt = f'{targets}\nWho would you like to use {thing.type.name} on? Enter the number of the character: '
                    if len(targets) > 1:
                        target_idx = prompt_user(prompt=prompt, invalid=lambda x: x not in range(len(cur_party)), fn=lambda x: int(x))
                    else:
                        target_idx = 0
                    target = cur_party[target]
            else:
                targets = op_toggle.get_party_members_names()
                prompt = f'{targets}\nWho would you like to use {thing.type.name} on? Enter the number of the character: '
                if len(targets) > 1:
                    target_idx = prompt_user(prompt=prompt, invalid=lambda x: x not in range(len(op_party)), fn=lambda x: int(x))                       
                else:
                    target_idx = 0
                clr_t()
                target = op_party[target_idx]
        
        elif action == 'give':
            action = prompt_user(f'Current Items\n 0: Potion:\n{player.get_item_type_str(ItemType.potion)}\n 1: Magic:\n{player.get_item_type_str(ItemType.magic)}\n 2: Armor:\n{player.get_item_type_str(ItemType.armor)}\n 3: Melee Weapon:\n{player.get_item_type_str(ItemType.melee)}\n 4: Ranged Weapon:\n{player.get_item_type_str(ItemType.ranged)}\nWhich kind of item do you want to give?',
                                 invalid=lambda x: type(x) is not ItemType,
                                 fn=lambda x: ItemType(int(x)))
            spacer = '\n\t'
            item_list = player.get_item_type(action)
            prompt = f'{player.name}\'s Current Items:{spacer}{"".join([str(i)+". "+str(x)+ spacer for i, x in enumerate(item_list)])}\nPlease enter the item that you want to give: '
            item_ind = prompt_user(prompt=prompt, invalid=lambda x: x not in range(len(item_list)), fn=lambda x: int(x))
            thing = item_list[item_ind]
            party_members = toggle.get_alive_players()
            target = prompt_user(prompt=f'{toggle.get_party_members_names()}\nEnter the number of the character to give the {item.type.name} to: ',
                                 invalid=lambda x: x not in range(len(party_members)),
                                 fn=lambda x : int(x))
            target = party_members[target]
        
        return  action, thing, target
    
    def play_turn(self, mode='enemy', debug=False, auto_play=False, data_parser=None):
        if verbose:
            print()
            if debug:
                print('Debug mode:', debug)
            if auto_play or mode == 'enemy':
                print(f'{mode} turn:')
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
            'buff': 0,
            'weapon': 0,
            'fist':0,
            'magic': 0,
        }
        cur_party = toggle.get_alive_players()
        for player in cur_party:
            use_log = {}
            #cur_party = toggle.get_alive_players()
            op_party = op_toggle.get_alive_players()
            cur_party_pow = toggle.get_power_level()
            op_party_pow = op_toggle.get_power_level()
            start_diff = cur_party_pow-op_party_pow
            if len(op_party) < 1: break
            if player.attr[PlayerStat.health] == 0: continue
            # create inputs for AI
            party_state = toggle.get_inputs()
            enemy_state = op_toggle.get_inputs()
            player_input = player.get_inputs()

            # print out all of the players that are still alive
            if debug and mode=='player':
                if verbose:
                    print(utils.colorize('Using Default Attack', 'red'))
                use_log = player.attack(random.choice(op_party))
                break

            # determine action to take 
            if mode == 'player':
                action, thing, target = self.get_player_action(player, toggle, op_toggle, cur_party, op_party)
            
            # random action for bot
            else:
                if mode in ['auto']:
                    state = {'player': player, 'friends': toggle, 'enemies': op_toggle}
                    action, thing, target = model_Auto.make_move(state)
                    assert False if action == 2 and thing.type == ItemType.melee and thing.uses == -99 else True, f'Ai tried to trade fist: {action}, {thing}' 
                elif mode in ['enemy']:
                    state = {'player': player, 'friends': toggle, 'enemies': op_toggle}
                    action, thing, target = model_Enemy.make_move(state)
                    assert False if action == 2 and thing.type == ItemType.melee and thing.uses == -99 else True, f'Ai tried to trade fist: {action}, {thing}'
                else:
                    action = random.choices(balance_dict['player']['possible_actions'], weights=balance_dict['player']['action_weight'])[0]

                    if action == 0:
                        target = random.choice(op_toggle.get_alive_players())
                        w_type = random.choice([3,4])
                        possible = player.get_item_type(ItemType(w_type))
                        if len(possible) == 0:
                            w_type = 3 if w_type == 4 else 4
                        possible = player.get_item_type(ItemType(w_type))
                        if len(possible) == 0:
                            possible = [item.Fist]
                        thing = random.choice(possible)

                    elif action == 1:
                        item_type = random.choice([0,1])
                        possible = player.get_item_type(ItemType(item_type))
                        if len(possible) == 0:
                            possible = player.get_item_type(ItemType.magic)
                        if len(possible) == 0:
                            possible = [item.Fist]
                        thing = random.choice(possible)
                        if thing.type != ItemType.potion and PlayerStat.attack in list(thing.effects.keys()):
                                target = random.choice(op_party)
                        else:
                            target = random.choice(cur_party)

                    elif action == 3:
                        target = player
                        thing = item.Pass

                    elif action == 2:
                        choices = player.get_item_type(ItemType(random.choice(range(5))))
                        assert item.Fist not in choices, 'fist was an option'
                        if len(choices) == 0:
                            thing = item.Fist
                            target = random.choice(op_party)
                            action = 0
                        else:
                            thing = random.choice(choices)
                            target = random.choice(cur_party)

                if verbose:
                    print(utils.colorize(f'{toggle.name}', 'red' if mode == 'enemy' else 'cyan'), utils.colorize(f'Team making action:', 'green'), utils.colorize(f'{action}', ['bold', 'on_cyan'] if action == 'use' else ['bold', 'on_green'] if action == 'pass' else ['bold', 'on_yellow'] if action == 'give' else ['bold', 'on_red']))

            targ_input = target.get_inputs()
            item_input = thing.get_inputs()
            action = action if type(action) is int else convert[action]
            # Action - Pass: regens HP, MP, STA
            if (action == 3) or (mode != 'player' and (player.attr[PlayerStat.mana] < player.attr[PlayerStat.level]/balance_dict['battle']['mana_thresh'] or player.attr[PlayerStat.stamina] < player.attr[PlayerStat.level]/balance_dict['battle']['stamina_thresh'])):
                use_log, st = self.pass_move(player=player, mode=mode, st=st)
                assert type(st) is dict and type(use_log) is dict, f'{action}, {st}, {use_log}'

            # Action - Attack
            elif action == 0:
                use_log, st = self.attack_move(player, mode, auto_play, st, thing, target)
                assert type(st) is dict and type(use_log) is dict, f'{action}, {st}, {use_log}'
            
            # Action - Use an Item
            elif action == 1:
                use_log, st = self.use_move(player, st, thing, target)
                assert type(st) is dict and type(use_log) is dict, f'{action}, {st}, {use_log}'
                
            # Action - Give item to teammate
            elif action ==  2:
                assert thing in player.items[thing.type], f'this {thing} was not in the inventory: {player.items[thing.type]}'
                use_log = self.give_move(player, thing, target)
                assert type(st) is dict and type(use_log) is dict, f'{action}, {st}, {use_log}'

            #assert type(st) is dict and type(use_log) is dict, f'{action}, {st}, {use_log}'
            end_cur_party_pow = toggle.get_power_level()
            end_op_party_pow = op_toggle.get_power_level()
            end_diff = end_cur_party_pow-end_op_party_pow
            reward = end_diff - start_diff
            state = party_state + enemy_state + player_input + targ_input + item_input + [action]
            if data_parser:
                data_parser.add_data(state, reward)
            st = agg(st, {'reward': reward})
            st = agg(st, use_log)

        return st

    def combat_round(self, debug=False, auto_play=False, data_save=None):
        # Player turn
        if auto_play:
            p_stats = self.play_turn(mode='auto', debug=debug, auto_play=auto_play, data_parser=data_save)
        else:
            p_stats = self.play_turn(mode='player')
        p_stats['moves'] = p_stats.get('moves',0) + len(self.player_party.get_alive_players())
        p_stats['turns'] = p_stats.get('turns',0) + 1
        # Enemy turn 
        e_stats = self.play_turn(mode='enemy', debug=debug, auto_play=auto_play, data_parser=data_save)

        e_stats['moves'] = e_stats.get('moves',0)  + len(self.enemy_party.get_alive_players())
        e_stats['turns'] = e_stats.get('turns',0) + 1
        self.validate()
        return p_stats, e_stats
    
    def start_game(self, debug=False, auto_play=False, readable=False, save_data=False):
        ts  = 0.00001 if not readable else 0.9
        p_stats = {}
        e_stats = {}
        data_parser = save_load.DataSaverLoader(save_location)
        if not (debug or auto_play):
            input('Press any key to begin the battle!')
            clr_t()

        while (self.player_party.get_alive_players() and self.enemy_party.get_alive_players()):
            a,b = self.combat_round(debug=debug, auto_play=auto_play, data_save=data_parser if save_data else None)
            p_stats = agg(p_stats, a)
            e_stats = agg(e_stats, b)
            if readable and debug:
                time.sleep(ts)
        
        p_stats = agg(p_stats, {'Wins': 1} if self.player_party.get_alive_players() else {'Losses': 1})
        e_stats = agg(e_stats, {'Wins': 1} if self.enemy_party.get_alive_players() else {'Losses': 1})
        
        if verbose:
            if not (debug or auto_play):
                clr_t()
                print("Combat over!")
                if len(self.player_party.get_alive_players()) > 0:
                    print('You won, Congratulations!')
                else:
                    print('You Lose, Weep in pain!')
        data_parser.save_data()
        del data_parser
        if not auto_play:
            return {'Player':p_stats, 'Enemy': e_stats}
        else:
            if verbose:
                print('Game Over')
            return p_stats, e_stats
        