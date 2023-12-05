import random
from . import party, g_vars, hypers, AI
ItemType = g_vars.ItemType
PlayerStat = g_vars.PlayerStat
StatColor = g_vars.StatColor
import os
import time
from game.gametests import utils
balance_dict = g_vars.config['balance']
item_hypers, player_hypers, meta_params = hypers.load_hypers()

verbose = g_vars.config['meta']['verbose']

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

    def attack_move(self, player, mode, op_party, op_toggle, debug, auto_play, st):
        # choosing a weapon from 'weapon_choice'
        if mode != 'player':
            ranged_possible = player.get_item_type(ItemType.ranged)
            melee_possible = player.get_item_type(ItemType.melee)
            weapon_choice = ranged_possible if len(ranged_possible) > len(melee_possible) else melee_possible
            target = op_party[-1]#random.choices(op_party, weights=[1/p.stats[PlayerStat.defense] for p in op_party])[0] # TODO: make a decision on which enemey is the best to attack
            if random.random() > 0.1 and len(weapon_choice) > 0:
                if len(weapon_choice) > 1:
                    weapon = 0 #random.choices([i for i in range(len(weapon_choice))], weights=[a.rank for a in weapon_choice])[0] # TODO: make a selection mechanism for items
                else:
                    weapon = 0
            else:
                weapon = -1
        #prompt user to choose a weapon
        else:
            weapon_type = prompt_user(f'Would you like to use:\n[0] Melee Weapon\n[1] Ranged Weapon\nEnter selection: ', 
                                      invalid=lambda x: x not in [ItemType.melee, ItemType.ranged],
                                      fn=lambda x: [ItemType.melee, ItemType.ranged][int(x)])
            weapon_choice = player.get_item_type(weapon_type)

            prompt = f'{player.get_item_type_str(weapon_type, spacer="", numbered=True)}-1. Fist - use base attack stat [ {player.stats[PlayerStat.attack]} ATK ]\nPlease Select a weapon to use: '
            weapon = prompt_user(prompt=prompt, invalid=lambda x: x not in range(-1,len(weapon_choice)), fn=lambda x: int(x))
            
            if len(op_party) > 1:
                prompt = op_toggle.get_party_members_names() + '\nWho would you like to attack? Enter the number of the character: '
                target_idx = prompt_user(prompt=prompt, invalid=lambda x: x not in range(len(op_party)), fn=lambda x: int(x))
                target = op_party[target_idx]
            else:
                target = op_party[0]
            if not debug:
                clr_t()
        use_armor=True
        # Player decide to use armor 
        if mode == 'enemy':
            if not auto_play:
                ans = prompt_user(f'{target.name} is being attacked... Use armor for extra DEF? [Y]/[N]: ', invalid=lambda x: x not in ['Y','N'], fn=lambda x: str.upper(x.split()[0]))
                use_armor = True if ans == 'Y' else False

        # Use weapon attack
        if weapon >= 0:
            st = agg(st, {'weapon':1})
            weapon = weapon_choice[weapon]
            use_log = player.use(weapon, target, use_armor=use_armor)
        # Use fist attack
        else:
            st = agg(st, {'fist':1})      
            use_log = player.attack(target, use_armor=use_armor)
        return use_log, st

    def use_move(self, player, mode, op_party, op_toggle, cur_party, st, action):
        # TODO: Make intelligent method of selecting moves
        # Random item to use for the bot
        if mode != 'player':
            target = op_party[-1]#random.choice(op_party)
            possible = []
            tries = 0
            while len(possible) == 0:
                possible = player.get_item_type(ItemType(random.choices([0, 1], weights=[0.35,0.65])[0]))
                tries += 1
                if tries > 20: break

            if len(possible) == 0:
                if verbose:
                    print('No items to use:')
                use_log = player.attack(target)
                return use_log, st

            if len(possible) > 2:
                item = random.choices(possible, weights=[it.rank for it in possible])[0]
            else:
                item = possible[0]
        # player Picks Item to use
        else:
            #print(action)
            spacer = '\n\t'
            item_type = ItemType(int(action.split()[1]))
            item_list = player.items[item_type] 
            prompt = f'{player.name}\'s Current Items:{spacer}{player.get_item_type_str(item_type, numbered=True)}\nPlease enter the item that you want to use: '
            item_ind = prompt_user(prompt=prompt, invalid=lambda x: x not in range(len(item_list)), fn=lambda x: int(x))
            item = item_list[item_ind]

        # Use potion or util magic
        if item.type == ItemType.potion or PlayerStat.attack not in item.effects.keys():
            st = agg(st, {'buff': 1})
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
                    if mode == 'player':
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
                    if mode == 'player':
                        clr_t()
                    use_log = player.use(item, cur_party[target_idx])
        
        # Use magic attack
        elif item.type == ItemType.magic:
            st = agg(st, {'magic': 1})

            # Bot randomly choses opponent
            if mode != 'player':
                use_log = player.use(item, random.choice(op_party)) 

            # Player chooses who to attack
            else:
                targets = op_toggle.get_party_members_names()
                prompt = f'{targets}\nWho would you like to use {item.type.name} on? Enter the number of the character: '
                if len(targets) > 1:
                    target_idx = prompt_user(prompt=prompt, invalid=lambda x: x not in range(len(op_party)), fn=lambda x: int(x))                       
                else:
                    target_idx = 0
                clr_t()
                use_log = player.use(item, op_party[target_idx])

        return use_log, st

    def give_move(self, player, mode, cur_party, toggle, op_party, action):
        # TODO: make this intelligent
        if mode != 'player':
            target = random.choice(cur_party)
            possible = []
            tries = 0
            while len(possible) == 0:
                possible = player.get_item_type(ItemType(random.choices([0, 1, 2, 3], weights=[0.25,0.25,0.25,0.25])[0]))
                tries += 1
                if tries > 20: break

            if len(possible) == 0:
                if verbose:
                    print('No items to give:')
                use_log = player.attack(random.choice(op_party))
                return use_log

            if len(possible) > 2:
                item = random.choices(possible, weights=[it.rank for it in possible])[0]
            else:
                item = possible[0]
        else:
            #print(action)
            action = prompt_user(f'Current Items\n 0: Potion:\n{player.get_item_type_str(ItemType.potion)}\n 1: Magic:\n{player.get_item_type_str(ItemType.magic)}\n 2: Armor:\n{player.get_item_type_str(ItemType.armor)}\n 3: Melee Weapon:\n{player.get_item_type_str(ItemType.melee)}\n 4: Ranged Weapon:\n{player.get_item_type_str(ItemType.ranged)}\nWhich kind of item do you want to give?',
                                 invalid=lambda x: type(x) is not ItemType,
                                 fn=lambda x: ItemType(int(x)))
            spacer = '\n\t'
            item_list = player.get_item_type(action)
            prompt = f'{player.name}\'s Current Items:{spacer}{"".join([str(i)+". "+str(x)+ spacer for i, x in enumerate(item_list)])}\nPlease enter the item that you want to give: '
            item_ind = prompt_user(prompt=prompt, invalid=lambda x: x not in range(len(item_list)), fn=lambda x: int(x))
            item = item_list[item_ind]
            party_members = toggle.get_alive_players()
            target = prompt_user(prompt=f'{toggle.get_party_members_names()}\nEnter the number of the character to give the {item.type.name} to: ',
                                 invalid=lambda x: x not in range(len(party_members)),
                                 fn=lambda x : int(x))
            target = party_members[target]
        player.give(item, target)
        return {'give':1}

    def play_turn(self, mode='enemy', debug=False, auto_play=False):
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
            op_party = op_toggle.get_alive_players()
            if len(op_party) < 1: break

            # print out all of the players that are still alive
            if debug and mode=='player':
                if verbose:
                    print(utils.colorize('Using Default Attack', 'red'))
                use_log = player.attack(random.choice(op_party))
                break

            # determine action to take 
            if mode == 'player':
                print(op_toggle.get_party_members_names())
                print(toggle.get_party_members_names())
                # prompt user to make a move
                if len(cur_party) < 2:
                    addon = ''
                else:
                    addon = '\n - To give an item to a party member type "give"'

                prompt = f'{player.name}\'s turn!\nHere is {player.name}\'s redout:\n{player}\n - To attack type "attack"\n - To use an item type "use (Item type #)"\n - To regen HP, MP, and STA type "pass"{addon}\nAction: '
                action = prompt_user(prompt=prompt, invalid=lambda x: x not in balance_dict['player']['possible_actions'] and len(x.split()) < 2)
            
            # random action for bot
            else:
                if mode == 'ai':
                    state = {'player': player, 'Enemies': op_party, 'friends': cur_party}
                    AI.make_move(state)
                else:
                    action = random.choices(balance_dict['player']['possible_actions'], weights=balance_dict['player']['action_weight'])[0]
                
                if verbose:
                    print(utils.colorize(f'{toggle.name}', 'red' if mode == 'enemy' else 'cyan'), utils.colorize(f'Team making action:', 'green'), utils.colorize(f'{action}', ['bold', 'on_cyan'] if action == 'use' else ['bold', 'on_green'] if action == 'pass' else ['bold', 'on_yellow'] if action == 'give' else ['bold', 'on_red']))

            # Action - Pass: regens HP, MP, STA
            if action == 'pass' or (mode != 'player' and (player.attr[PlayerStat.mana] < player.attr[PlayerStat.level]/balance_dict['battle']['mana_thresh'] or player.attr[PlayerStat.stamina] < player.attr[PlayerStat.level]/balance_dict['battle']['stamina_thresh'])):
                use_log, st = self.pass_move(player=player, mode=mode, st=st)
                assert type(st) is dict and type(use_log) is dict, f'{action}, {st}, {use_log}'

            # Action - Attack
            elif action == 'attack':
                use_log, st = self.attack_move(player, mode, op_party, op_toggle, debug, auto_play, st)
                assert type(st) is dict and type(use_log) is dict, f'{action}, {st}, {use_log}'
            
            # Action - Use an Item
            elif action.startswith('use'):
                use_log, st = self.use_move(player, mode, op_party, op_toggle, cur_party, st, action)
                assert type(st) is dict and type(use_log) is dict, f'{action}, {st}, {use_log}'
                
            # Action - Give item to teammate
            elif action == 'give':
                use_log = self.give_move(player, mode, cur_party, toggle, op_party, action)
                assert type(st) is dict and type(use_log) is dict, f'{action}, {st}, {use_log}'

            #assert type(st) is dict and type(use_log) is dict, f'{action}, {st}, {use_log}'

            st = agg(st, use_log)

        return st

    def combat_round(self, debug=False, auto_play=False):
        # Player turn
        if auto_play:
            p_stats = self.play_turn(mode='auto', debug=debug, auto_play=auto_play)
            p_stats['score'] = sum([])
        else:
            p_stats = self.play_turn(mode='player')
        p_stats['moves'] = p_stats.get('moves',0) + len(self.player_party.get_alive_players())
        p_stats['turns'] = p_stats.get('turns',0) + 1
        # Enemy turn 
        e_stats = self.play_turn(mode='enemy', debug=debug, auto_play=auto_play)
        e_stats['moves'] = e_stats.get('moves',0)  + len(self.enemy_party.get_alive_players())
        e_stats['turns'] = e_stats.get('turns',0) + 1
        self.validate()
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
        
        if verbose:
            if not (debug or auto_play):
                clr_t()
                print("Combat over!")
                if len(self.player_party.get_alive_players()) > 0:
                    print('You won, Congratulations!')
                else:
                    print('You Lose, Weep in pain!')

        if not auto_play:
            return {'Player':p_stats, 'Enemy': e_stats}
        else:
            if verbose:
                print('Game Over')
            return p_stats, e_stats
        