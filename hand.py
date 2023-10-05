VALUES = {
    "A": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "T": 10,
    "J": 10,
    "Q": 10,
    "K": 10,
}


class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        value = 0
        isAcePresent = False

        for i in self.cards:
            value = value + VALUES[i.get_rank()]

            if value == 1:
                isAcePresent = True

        if (isAcePresent) and ((value + 10) <= 21):
            value = value + 10

        return value

    def get_cards(self):
        return self.cards

   
