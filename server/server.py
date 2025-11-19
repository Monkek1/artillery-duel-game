from server.network import NetworkServer
from server.protocol import (
    create_chat_message,
    create_signup_message,
    create_exit_message,
)

# точка запуска сервера игры
def main():
    # создаем сервер, который слушате все подключения на этих хосте и порту
    server = NetworkServer(host="0.0.0.0", port=5000)

    #TODO: доделать методы когда будет реализован game_manager

    '''Пока методы просто работают как логи, потому что игровой логики нет'''
    #принятие подключения
    def handle_connect(client):
        print(f"Клиент подключился: {client.address}")

    #принятие сообщений
    #на вход принимаются объект ClientConnection и сообщенние в виде словаря
    #поэтому из сообщения можно получать поля через get
    def handle_message(client, msg):
        print(f"Адрес: {client.address}: {msg}")

        # достаем из сообщения его тип и решаем что делать в зависимости от него
        msg_type = msg.get("type")

        if msg_type == "signup":
            # достаем из сообщения имя
            name = msg.get("name")
            server.broadcast(
                create_chat_message(f"{name} вошёл в игру")
            )
        elif msg_type == "exit_game":
            server.broadcast(
                create_chat_message("Игрок покинул игру")
            )
        else:
            server.broadcast(msg)

    #принятие отключения
    def handle_disconnect(client):
        print(f"Клиент подключился: {client.address}")

    #тут мы и реализуем функции, которые заданы еще в server/network.py
    server.on_connect = handle_connect
    server.on_message = handle_message
    server.on_disconnect = handle_disconnect

    #запускаем сервер и начинаем слушать подключения
    server.start()
    input("Сервер запущен. Нажмите для выхода...\n")


if __name__ == "__main__":
    main()
