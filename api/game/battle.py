import random
from game import party

class Battle:
    # a battle is started between two parties 
    def __init__(self, p_args, e_args):
        self.player_party = party.Party(p_args)
        self.enemy_party = party.Party(e_args)

    # overall game loop to play the back and forth turns
    def play_game(self):

        # play game until one party is dead
        while not (self.player_party.dead or self.enemy_party.dead):
            run = self.player_turn()
            if run:
                break
            self.enemy_turn()

        return 1 if self.player_party.dead else 0


    def player_turn(self):
        pass

    def enemy_turn(self):
        pass