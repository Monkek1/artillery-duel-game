from server.network import NetworkServer

server = NetworkServer()
def on_msg(client, msg): print("server got:", msg)
server.on_message = on_msg
server.start()
input("Ввод для завершения")