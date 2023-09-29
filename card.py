
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')

class Card:
   

    def __init__(self, suit, rank, state):

        if (suit in SUITS) and (rank in RANKS) and state == 1:

            self.suit = suit
            self.rank = rank
            self.state = state

        else:

            self.suit = None
            self.rank = None
            self.state = None
            # print ("Carta Inválida: ", suit, rank)

    def __str__(self):

        return self.suit + self.rank

    def get_suit(self):

        return self.suit

    def get_rank(self):

        return self.rank

    def get_state(self):
        
        return self.state
    
    def set_state(self, state):

        self.state = state