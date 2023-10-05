import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from tkinter import simpledialog


CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')

class BjGUI:
    def __init__(self, blackjack) -> None:
        self.blackjack = blackjack
        self.user_name = None
        self.playerIndex = None 
        pass
    
    def draw_card(self, suit, rank, canvas, pos):

        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(rank),
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)


    def draw_hand(self, cards, canvas, pos):

        j = 0
            
        for i in cards:
            self.draw_card(i["suit"], i["rank"], canvas, [(pos[0] + (j * 80)), pos[1]])
            j = j + 1

    def draw(self, canvas):
        canvas.draw_text("Blackjack", (210, 70), 48, 'Black')
        canvas.draw_text("Apuesta: " + str(self.blackjack.get_bet(self.blackjack.get_player_index(self.user_name))), (250, 110), 32, 'Black')
        canvas.draw_text("Banca:", (100, 180), 32, 'Black')
        canvas.draw_text("Jugador: "+ self.user_name, (100, 390), 32, 'Black')
        canvas.draw_text("Monto: "+ str(self.blackjack.get_ammount(self.blackjack.get_player_index(self.user_name))), (395, 390), 32, 'Black')
        self.draw_hand(self.blackjack.get_dealers_cards(), canvas, [100, 210])
        self.draw_hand(self.blackjack.get_players_cards(self.blackjack.get_player_index(self.user_name)), canvas, [100, 420])
        canvas.draw_text(self.blackjack.get_outcome(self.blackjack.get_player_index(self.user_name)), (80, 560), 34, 'Black')

        if self.blackjack.get_cover(self.blackjack.get_player_index(self.user_name)) == 1:

            canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [136.5, 259], CARD_SIZE)


    def showFrame(self):
       
        self.frame = simplegui.create_frame("Blackjack", 800, 600)
        self.frame.set_canvas_background("Darkgreen")

        #create buttons and canvas callback
        # print(playerIndex)
        self.frame.add_button("Abandonar Mesa", self.leave, 200)
        self.frame.add_button("Pedir",  self.take_turn, 200)
        self.frame.add_button("Plantarse", self.stand, 200)
        self.frame.add_button("Apostar + $100", self.bet, 200)
        self.frame.set_draw_handler(self.draw)

        # get things rolling
        
        self.frame.start()

    def deal(self):
        self.blackjack.deal()

    def take_turn(self):
        self.blackjack.take_turn(self.blackjack.get_player_index(self.user_name))

    def bet(self):
        self.blackjack.bet(self.blackjack.get_player_index(self.user_name))

    def hit(self):
        self.blackjack.hit(self.blackjack.get_player_index(self.user_name))
    
    def stand(self):
        self.blackjack.stand_turn(self.blackjack.get_player_index(self.user_name))

    def input_name(self):
    #    the input dialog
    
        self.user_name = simpledialog.askstring(title="Blackjack", prompt="Bienvenido a Blackjack - Escribe tu Nombre")
        
        
        return self.user_name

    def leave(self):
        self.blackjack.leave(self.blackjack.get_player_index(self.user_name))
        self.frame.stop()