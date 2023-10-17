from Pyro5 import nameserver
import socket

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
print(hostname, IPAddr)
nameserver.start_ns_loop(
    host='172.16.110.210',
    port=9090,
    bcport=9091,
    bchost='172.16.110.210',
    enableBroadcast=True,
)
