from client.network import NetworkClient
from client.protocol import create_chat_message

c = NetworkClient()
c.on_message = lambda m: print("client got:", m)
c.connect()
c.send(create_chat_message("hi"))
