# Blackjack Card Game


# from card import Card
from deck import Deck
from hand import Hand
from player import Player

# define event handlers for buttons
import Pyro5.api
from threading import Timer
from DBconnector import DBconnectSingleton


@Pyro5.api.expose
class Blackjack:
    players = []
    card = None
    deck = []
    dealer = []
    turn = 0
    in_play = []
    cover = 0
    

    @Pyro5.api.expose
    def join_game(cls, playerName):

        ammount = DBconnectSingleton().get_one_ammount(playerName)
      
        if ammount!=-1:
            player = Player(playerName, ammount)
        else:
            player = Player(playerName, 10000)
        cls.players.append(player)
        # print(*cls.players)
        
        cls.deal()
       

    @Pyro5.api.expose
    def take_turn(cls, playerIndex):
        player = cls.players[playerIndex]
        if player.bet != 0:
            if not player.turn:
                player.outcome = "Esperando a otro jugador"
                return "No es tu turno."
            cls.hit(playerIndex)

    @Pyro5.api.expose
    def stand_turn(cls, playerIndex):
        player = cls.players[playerIndex]
        if player.bet != 0:
            if not player.turn:
                player.outcome = "Esperando a otro jugador"
                return "No es tu turno."
            cls.stand(playerIndex)

    @Pyro5.api.expose
    def bet(cls, playerIndex):
        player = cls.players[playerIndex]
        if not player.turn:
            player.outcome = "Esperando a otro jugador"
            return "No puedes apostar."
        player.bet += 100
        player.ammount -= 100

        DBconnectSingleton().update_all(cls.deck[0], cls.players)

    @Pyro5.api.expose
    def deal(cls):
        # if cls.deck and cls.players:
        #     print("Quedan " + str(len(cls.deck[0].cards)) + " cartas en el mazo")
        #     print("Necesito " + str(2 + len(cls.players) * 2) + " cartas para repartir")
        #     print("Mazos:" + str(len(cls.deck)))
        # if not cls.in_play:
        if not cls.deck or len(cls.deck[0].cards) < 2 + len(cls.players) * 2:
            cls.shuffle()
            # print("Nuevo Mazo")
            # print("Mazos:" + str(len(cls.deck)))
        # Reparte al Dealer

        
        
        if not cls.in_play:
            new_dealer = Hand()
            if not cls.dealer:
                cls.dealer.clear()
                cls.dealer.append(new_dealer)
            else:
                cls.dealer[0] = new_dealer
            cls.dealer[0].add_card(cls.deck[0].deal_card())
            cls.dealer[0].add_card(cls.deck[0].deal_card())
            cls.in_play.append(1)
        # print("Nuevo Dealer")

        # Reparte a los jugadores
        
        for i in cls.players:
            if not i.in_play:
                new_hand = Hand()
                i.hand = new_hand
                i.hand.add_card(cls.deck[0].deal_card())
                i.hand.add_card(cls.deck[0].deal_card())
                i.cover = 1
                i.outcome = "Pedir o Plantarse?"
                i.in_play = True
                i.turn = False

        cls.players[0].turn = True
        
        DBconnectSingleton().update_all(cls.deck[0], cls.players)

    def shuffle(cls):
        new_deck = Deck()
        cls.deck.clear()
        cls.deck.append(new_deck)
        cls.deck[0].shuffle()
       

    @Pyro5.api.expose
    def hit(cls, playerIndex):
        player = cls.players[playerIndex]
        # print("Quedan " + str(len(cls.deck[0].cards)) + " cartas en el mazo")
        # print("Necesito " + str(2 + len(cls.players) * 2) + " cartas para repartir")
        if player.in_play:
            if len(cls.deck[0].cards) < 1:
                cls.shuffle()

            cls.card = cls.deck[0].deal_card()
            player.hand.add_card(cls.card)

            if player.hand.get_value() > 21:
                player.in_play = False
                player.outcome = "Te pasaste! Perdiste!"
                player.bet = 0
                
                

                if player == cls.players[-1]:
                    cls.show_outcome()
                    cls.players[0].turn = True
                    t = Timer(3, cls.deal)
                    t.start()
                else:
                    cls.players[playerIndex].turn = False
                    cls.players[playerIndex + 1].turn = True
                    cls.players[playerIndex + 1].outcome = "Ya Puedes Jugar!"
        DBconnectSingleton().update_all(cls.deck[0], cls.players)



    def show_outcome(cls):
        for player in cls.players:
            player.cover = 0
            if player.in_play:
                if cls.dealer[0].get_value() > 21:
                    player.outcome = "Ganaste! Repartiendo..."
                    player.in_play = False
                    player.ammount += player.bet * 2
                    player.bet = 0

                else:
                    if cls.dealer[0].get_value() >= player.hand.get_value():
                        player.outcome = "Perdiste! Repartiendo..."
                        player.in_play = False
                        player.bet = 0

                    else:
                        player.outcome = "Ganaste! Repartiendo..."
                        player.in_play = False
                        player.ammount += player.bet * 2
                        player.bet = 0
        DBconnectSingleton().update_all(cls.deck[0], cls.players)

    @Pyro5.api.expose
    def dealer_play(cls):
        while cls.dealer[0].get_value() < 17:
            if len(cls.deck[0].cards) < 1:
                cls.shuffle()
            cls.card = cls.deck[0].deal_card()
            cls.dealer[0].add_card(cls.card)
        cls.in_play.clear()
        cls.show_outcome()

        t = Timer(3, cls.deal)
        t.start()

    @Pyro5.api.expose
    def stand(cls, playerIndex):
        # print(cls.get_player_index(cls.players[-1].name))
        if playerIndex == cls.get_player_index(cls.players[-1].name):
            cls.dealer_play()
            cls.players[0].turn = True

        else:
            cls.players[playerIndex].outcome = "Plantaste! Esperando a otro jugador"
            cls.players[playerIndex].turn = False
            cls.players[playerIndex + 1].turn = True
            cls.players[playerIndex + 1].outcome = "Ya Puedes Jugar!"

    @Pyro5.api.expose
    def leave(cls, playerIndex):
        cls.players.pop(playerIndex)
        

    @Pyro5.api.expose
    def get_dealers_cards(cls):
        cards = cls.dealer[0].get_cards()
        cards2 = []
        for i in cards:
            cards2.append(vars(i))
        return cards2

    @Pyro5.api.expose
    def get_players_cards(cls, playerIndex):
        player = cls.players[playerIndex]
        cards = player.hand.get_cards()
        cards2 = []
        for i in cards:
            cards2.append(vars(i))
        return cards2

    @Pyro5.api.expose
    def get_player_index(cls, playerName):
        # print(playerName)
        for index, item in enumerate(cls.players):
            if item.name == playerName:
                return index

    # Getter y Setter para "outcome"
    @Pyro5.api.expose
    def get_outcome(cls, playerIndex):
        player = cls.players[playerIndex]
        return player.outcome

    @Pyro5.api.expose
    def set_outcome(cls, outcome, playerIndex):
        player = cls.players[playerIndex]
        player.outcome = outcome

    @Pyro5.api.expose
    def get_ammount(cls, playerIndex):
        player = cls.players[playerIndex]
        return player.ammount

    @Pyro5.api.expose
    def set_ammount(cls, ammount, playerIndex):
        player = cls.players[playerIndex]
        player.ammount = ammount

    # Getter y Setter para "deck"
    @Pyro5.api.expose
    def get_deck(cls):
        return cls.deck

    @Pyro5.api.expose
    def set_deck(cls, deck):
        cls.deck = deck

    # Getter y Setter para "hand"
    @Pyro5.api.expose
    def get_hand(cls):
        return cls.hand

    @Pyro5.api.expose
    def set_hand(cls, hand):
        cls.hand = hand

    @Pyro5.api.expose
    def get_bet(cls, playerIndex):
        player = cls.players[playerIndex]
        return player.bet

    @Pyro5.api.expose
    def set_bet(cls, bet, playerIndex):
        player = cls.players[playerIndex]
        player.bet = bet

    # Getter y Setter para "dealer"
    @Pyro5.api.expose
    def get_dealer(cls):
        return cls.dealer

    @Pyro5.api.expose
    def set_dealer(cls, dealer):
        cls.dealer = dealer

    # Getter y Setter para "cover"
    @Pyro5.api.expose
    def get_cover(cls, playerIndex):
        player = cls.players[playerIndex]
        return player.cover

    @Pyro5.api.expose
    def set_cover(cls, cover):
        cls.cover = cover

    @Pyro5.api.expose
    def get_dealer_cover(cls):
        return cls.cover
