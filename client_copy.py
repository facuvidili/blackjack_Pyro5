
import logging
logging.basicConfig()  # or your own sophisticated setup
logging.getLogger("Pyro5").setLevel(logging.DEBUG)
logging.getLogger("Pyro5.core").setLevel(logging.DEBUG)

import Pyro5.api
import socket
from bjgui import BjGUI

agenda = {"nabil": "DESKTOP-GDMDAN5",
          "facundo":"Chimi",
          "martin":"DESKTOP-09V1F9E",
          "tomas":"AN515",
          "pablo":"Pablo-Notebook"}

ns = Pyro5.core.locate_ns(host=socket.gethostbyname(agenda["tomas"]) , port=9090)

uri = ns.lookup("blackjack")

blackjack = Pyro5.client.Proxy(uri)

bjGui = BjGUI(blackjack)

user = bjGui.input_name()

if(user):
    blackjack.join_game(user, 10000)

bjGui.showFrame()