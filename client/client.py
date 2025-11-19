from client.network import NetworkClient
from server.protocol import (
    create_chat_message,
    create_signup_message,
    create_exit_message,
)

# точка запуска клиента
def main():
    # создаем исходящее подключение от клиента
    client = NetworkClient()

    #TODO: доделать методы когда игровая логика будет, пока они логи просто пишут

    #при подсоединении
    def on_connect():
        print("Подключился к серверу")
        name = input("Введите ваше имя: ")
        client.send(create_signup_message(name))

    #при сообщении от пользователя
    def on_message(msg):
        print("От сервера:", msg)

    #при отключении
    def on_disconnect():
        print("Отключился от сервера")

    #тут назначем функции которые были ничем в нетворкклайент
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect

    #подключаемся к серверу
    client.connect()

    #запускаем бесконечный цикл чтения из консоли от клиента
    #который прерывает если пользователь выходит
    try:
        while True:
            text = input("")
            if text.strip().lower() in ("/exit"):
                client.send(create_exit_message())
                break
            #чат сообщение
            client.send(create_chat_message(text))
    except KeyboardInterrupt:
        pass
    #в любом случае отключаемся
    finally:
        client.close()


if __name__ == "__main__":
    main()
