import Pyro5.api
from tkinter import messagebox as mb

from bjgui import BjGUI


def conectar(main_name_server, backup_name_server=None):
    try:
        # agenda = {"facundo":"Chimi",
        #     "backup":"facu-2949"}
        ns = Pyro5.core.locate_ns(main_name_server, port=9090)
        uri = ns.lookup("server")
        server = Pyro5.client.Proxy(uri)
    except Pyro5.errors.NamingError as e:
        print((f"Error al conectarse al servidor => " + main_name_server + ": " + {e}))
    if backup_name_server is not None:
        server.set_backup(backup_name_server)
    return server


server = conectar("192.168.100.29", "192.168.100.7")

try:
    bjGui = BjGUI(server)

    while True:
        user = bjGui.input_name()
        players = server.get_players()
        if not user in players:
            msg = server.join_game(user)
            bjGui.showFrame()
            break
        else:
            mb.showerror(message="Usuario ya activo. Elija otro nombre")

except Exception:
    print("Error! conectando con servidor de backup...")
    server = conectar("192.168.100.7")
