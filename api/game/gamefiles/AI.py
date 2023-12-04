from . import g_vars, hypers
ItemType = g_vars.ItemType
PlayerStat = g_vars.PlayerStat


def make_move(state) -> str:
    cur_player = state['player']
    cur_team = state['friends']
    op_team = state['enemy']
    
    our_rank = cur_team.get_power_level()
    their_rank = op_team.get_power_level()

    my_health = cur_player.stats[PlayerStat.health]
    my_stamina = cur_player.stats[PlayerStat.health]
    my_mana = cur_player.stats[PlayerStat.health]
    my_rank = cur_player.rank

    best_potion = cur_player.items[ItemType.potion]
    best_magic = cur_player.items[ItemType.potion]
    best_ranged = cur_player.items[ItemType.potion]
    best_melee = cur_player.items[ItemType.potion]

    possible_targets = [p for p in op_team if p.rank < my_rank]

    if our_rank > their_rank:
        # we are currently expected to win
        if  my_health < 10:
            return 'pass'
        elif my_stamina > 30:
            return 'attack'
    else:
        # we are currently expected to lose
        if my_health < 10:
            return 'pass'