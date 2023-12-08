
from backend.classes import party, player, item
from game.gamefiles import g_vars

stats = g_vars.stats

Dike_Tyson_Party = party.Party(members=[player.Player(stats={stats[0]: 41, stats[1]: 43, stats[2]: 39,stats[3]: 33,stats[4]: 31}, 
                                                      attr={stats[5]: 100, stats[6]: 100, stats[7]: 100,stats[8]: 75, 'name':'Dike Tyson'}, 
                                                      items=item.generate_items(n_items=12, level=75))
                                        ],
                               name='Dike Tyson\'s Squad')

Enemy_Test_Party = party.Party(members=[player.Player(stats={stats[0]: 45, stats[1]: 39, stats[2]: 38,stats[3]: 31,stats[4]: 35}, 
                                                      attr={stats[5]: 100, stats[6]: 100, stats[7]: 100,stats[8]: 75, 'name':'stefGPT'}, 
                                                      items=item.generate_items(n_items=12, level=75))
                                        ],
                               name='Enemy Test')