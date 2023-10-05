from Pyro5 import nameserver
import socket

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
print(hostname, IPAddr)
nameserver.start_ns_loop(
    host="192.168.100.29",
    port=9090,
    bcport=9091,
    bchost="192.168.100.29",
    enableBroadcast=True,
)
