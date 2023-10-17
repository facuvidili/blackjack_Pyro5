from Pyro5.api import expose, behavior, serve
import Pyro5.api
import socket

from blackjack import Blackjack


@expose
@behavior(instance_mode="single")
class Server:
    def __init__(self):
        self.blackjack = Blackjack()
        self.__backup = None

    def set_backup(self, backup_hostname):
        try:
            agenda = {"facundo":"Chimi",
            "tomas":"AN515"}
            ns = Pyro5.core.locate_ns(backup_hostname, port=9090)
            #print(ns.list(return_metadata=True))
            uri = ns.lookup("server")
            self.__backup = Pyro5.client.Proxy(uri)
            print("backup conectado: " + backup_hostname)
        except Pyro5.errors.NamingError as e:
            print((f"Error al conectarse al servidor => " + backup_hostname + ": " + {e}))

    def get_players(self):
        return self.blackjack.get_players()

    def get_player_index(self, user_name):
        return self.blackjack.get_player_index(user_name)

    def get_bet(self, playerIndex):
        return self.blackjack.get_bet(playerIndex)

    def get_ammount(self, playerIndex):
        return self.blackjack.get_ammount(playerIndex)

    def get_dealers_cards(self):
        return self.blackjack.get_dealers_cards()

    def get_players_cards(self, playerIndex):
        return self.blackjack.get_players_cards(playerIndex)

    def get_outcome(self, playerIndex):
        return self.blackjack.get_outcome(playerIndex)

    def get_cover(self, playerIndex):
        return self.blackjack.get_cover(playerIndex)

    def join_game(self, playerName):
        self.blackjack.join_game(playerName)

    def deal(self):
        self.blackjack.deal()

    def take_turn(self, playerIndex):
        self.blackjack.take_turn(playerIndex)

    def stand_turn(self, playerIndex):
        self.blackjack.stand_turn(playerIndex)

    def bet(self, playerIndex):
        self.blackjack.bet(playerIndex)

    def hit(self, playerIndex):
        self.blackjack.hit(playerIndex)

    def stand(self, playerIndex):
        self.blackjack.stand_turn(playerIndex)

    def leave(self, playerIndex):
        self.blackjack.leave(playerIndex)

    def set_blackjack(self, blackjack):
        self.blackjack = blackjack


hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
print(hostname, IPAddr)
# name_server = NameServerSingleton(IPAddr)
serve(
    {
        Server: "server",
    },
    host='172.16.110.210',
    port=9092,
    verbose=True,
)
print("server down")
