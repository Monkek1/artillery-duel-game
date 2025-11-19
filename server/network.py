import socket
import threading
from server.protocol import serialize_message, deserialize_message

#подключение для одного клиента
#тут сокет, который принимает входящее подключение от клиента
class ClientConnection:
    def __init__(self, socket, address, server):
        self.socket = socket #tcp сокет
        self.address = address #ip адрес и порт
        self.server = server #networkserver
        self.alive = True #подключен ли клиент

    # запускаем поток, который слушает данные от клиента
    # на фоне из сокета
    def start(self):
        thread = threading.Thread(target=self.listen, daemon=True)
        thread.start()

    def listen(self):
        try:
            while self.alive:
                data = self.socket.recv(4096)
                if not data:
                    break

                message = deserialize_message(data)
                self.server.on_message(self, message)

        except Exception as e:
            print(f"Ошибка у клиента {self.address} : {e}")
    
        #в любом случае закрываем соединение
        finally:
            self.close()

    #отправка сообщений клиенту по сокету
    def send(self, message):
        try:
            self.socket.sendall(serialize_message(message))
        except:
            self.close()

    #закрытие соккета
    def close(self):
        if self.alive:
            self.alive = False
            self.socket.close()
            self.server.on_disconnect(self)
            print(f"Клиент отключился: {self.address}")

#сам сервер (не точка запуска сервера)
#тут слушающий сокет, который принимает новые подключения и создает парные
# сокеты
class NetworkServer:
    def __init__(self, host="0.0.0.0", port=5000):
        self.host = host
        self.port = port
        self.server_socket = None
        self.clients = []

        # эти функции связываются с server.py, который
        # передает эти сообщения game_manager.py 
        self.on_message = lambda client, msg: None
        self.on_connect = lambda client: None
        self.on_disconnect = lambda client: None

    #создание и запуск слушающего порт сокета
    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        print(f"Запущен на {self.host}:{self.port}")

        #начинаем принимать подключяющихся клиентов
        threading.Thread(target=self.accept_clients, daemon=True).start()

    def accept_clients(self):
        while True:
            #здесь создается соединение сервер-клиент
            client_sock, addr = self.server_socket.accept()
            print(f"Подключился клиент: {addr}")

            # передаем TCP-соедниение и адрес клиента в наше входящее подключение
            conn = ClientConnection(client_sock, addr, self)
            # добавление этого клиента в список
            self.clients.append(conn)
            # сообщение серверу что клиент подключился
            self.on_connect(conn)
            # запуск демон потока который принимает сообщения от клиента
            conn.start()

    #отправка сообщений клиентам
    def broadcast(self, message):
        for c in list(self.clients):
            c.send(message)
