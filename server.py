import Pyro5.api
import socket 
from nameserver import NameServerSingleton
from blackjack import Blackjack


hostname=socket.gethostname()   
IPAddr=socket.gethostbyname(hostname)

name_server = NameServerSingleton(IPAddr)

daemon = Pyro5.server.Daemon(host=IPAddr, port=9092)       
uri = daemon.register(Blackjack)  
Pyro5.api.locate_ns().register("blackjack", uri) 

print("Server Ready!")
daemon.requestLoop()                   
