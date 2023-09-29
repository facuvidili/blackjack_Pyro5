class Player:
    
    def __init__(self, name, ammount=10000):

        self.name = name
        self.index = None
        self.ammount = ammount
        self.hand = None
        self.cover = 0
        self.outcome = ""
        self.in_play = False
        self.turn = False
        self.bet = 0


    def __str__(self):

        return "Jugador: " + self.name + "; Cuenta: " + self.ammount
    
    def get_ammount(self):
        
        return self.ammount

    def get_hand(self):
        return self.hand
    
    def set_hand(self, hand):
        self.hand = hand

    def get_name(self):
        return self.name