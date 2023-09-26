from Pyro5 import nameserver
from threading import Thread

class NameServerSingleton:
    _instance = None

    def __new__(self, IPAddr):
        if self._instance is None:
            self._instance = super().__new__(self)
            # Iniciar el servidor de nombres Pyro5
            def execNS():
                ns=nameserver.start_ns_loop(host=IPAddr, port=9090, bcport=9091, bchost=IPAddr, enableBroadcast=True)
                
            hilo = Thread(target=execNS, args=[])
            hilo.start()
            
        return self._instance

