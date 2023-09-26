import random
from card import Card
from DBconnector import DBconnectSingleton


class Deck:

    def __init__(self):

        self.cards = []

        cards = DBconnectSingleton().get_all("tipoCarta, valorCarta, estado", "mazo")
        

        for i in cards:
            self.cards.append(Card(i[0],i[1],i[2]))

    def shuffle(self):

        random.shuffle(self.cards)

    def deal_card(self):

        return self.cards.pop()

    def __str__(self):

        s = "Cartas en el mazo: "

        for i in self.cards:

            s = s + str(i) + " "

        return s
    
    