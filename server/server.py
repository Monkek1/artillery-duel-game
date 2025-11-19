from server.network import NetworkServer
from server.protocol import (
    create_chat_message,
    create_signup_message,
    create_exit_message,
)
from server.game_manager import GameManager

# точка запуска сервера игры
def main():
    # создаем сервер, который слушате все подключения на этих хосте и порту
    # создаем менеджер игры, который работает с игровой логикой
    server = NetworkServer(host="0.0.0.0", port=5000)
    game = GameManager()

    #принятие подключения
    def handle_connect(client):
        print(f"Клиент подключился: {client.address}")

    #принимаем входящее подключение от игрока
    #и слушаем от него сообщения
    #которые передаем игровой логике
    def handle_message(client, msg):
        print(f"From {client.address}: {msg}")

        msg_type = msg.get("type")

        #при заходе
        if msg_type == "signup":
            name = msg.get("name", "Игрок")
            #превращаем входящее подключение в объект игрока для 
            #гейм менеджера и добавляем в список игроков в 
            #игровом менеджере (не путать со списком клиентов)
            game.add_player(client, name)
            server.broadcast(
                create_chat_message(f"{name} присоединился к игре")
            )
            #обновляем состояние игры для всех клиентов
            server.broadcast(game.build_state())

        elif msg_type == "move":
            x = msg.get("x")
            y = msg.get("y")
            game.handle_move(client, x, y)
            #обновляем состояние игры для всех клиентов
            server.broadcast(game.build_state())

        elif msg_type == "exit_game":
            game.remove_player(client)
            server.broadcast(
                create_chat_message("Игрок покинул игру")
            )
            #обновляем состояние игры для всех клиентов
            server.broadcast(game.build_state())

        else:
            server.broadcast(msg)

    def handle_disconnect(client):
        print(f"Клиент отключился: {client.address}")
        game.remove_player(client)
        #обновляем состояние игры для всех клиентов
        server.broadcast(game.build_state())

    #тут мы и реализуем функции, которые заданы еще в server/network.py
    server.on_connect = handle_connect
    server.on_message = handle_message
    server.on_disconnect = handle_disconnect

    #запускаем сервер и начинаем слушать подключения
    server.start()
    input("Сервер запущен. Нажмите для выхода...\n")


if __name__ == "__main__":
    main()

