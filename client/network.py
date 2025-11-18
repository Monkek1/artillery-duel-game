import socket
import threading
from server.protocol import serialize_message, deserialize_message

#управление сокетом клиента
class NetworkClient:
    def __init__(self, host="127.0.0.1", port=5000):
        #адрес и порт сервера, к которому будет подключаться
        self.host = host
        self.port = port
        #сначала сокет пустой
        self.socket = None
        #подключен ли клиент
        self.alive = False

        # функции, которые реализованы в client.py
        self.on_message = lambda msg: None
        self.on_connect = lambda: None
        self.on_disconnect = lambda: None


    def connect(self, host=None, port=None):
        if self.alive:
            return

        # переданы или не переданы аргументы
        self.host = host or self.host
        self.port = port or self.port

        # создаем сокет для клиента на IPv4 TCP и подключаеся по айпи и порту
        # тут сокет, который принимает исходящее подключение от клиента
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.alive = True

        #запускаем фоновый поток, который слушает сокет
        self.on_connect()
        threading.Thread(target=self._listen, daemon=True).start()

    #слушаем сокет и принимаем данные которые передаем в client и потом в gui 
    # и обратно
    def _listen(self):
        try:
            while self.alive:
                data = self.socket.recv(4096)
                if not data:
                    break
                msg = deserialize_message(data)
                self.on_message(msg)
        except Exception as e:
            print(f"Client listen error: {e}")
        finally:
            self.close()

    def send(self, message):
        if not self.alive:
            raise RuntimeError("Client is not connected")
        try:
            self.socket.sendall(serialize_message(message))
        except Exception as e:
            print(f"Send failed: {e}")
            self.close()

    #отключение клиента
    def close(self):
        if not self.alive:
            return
        self.alive = False
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
        except Exception:
            pass
        try:
            self.socket.close()
        except Exception:
            pass
        self.on_disconnect()
