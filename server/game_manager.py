from server.protocol import create_game_state_message

#объект игрок для гейм менеджера, превращаем clientconnection
#в игрока для гейм менеджера
class Player:
    def __init__(self, client, name="Игрок"):
        self.client = client
        self.name = name

        #горизонтальная координата и здоорвье
        self.x = 0
        self.y = 0
        self.hp = 100

#гейм менеджер это объект, который хранит в себе всё что есть
#логически в игре, и это можно менять через файл сервера
class GameManager:

    #TODO: Доделать менеджер игры когда появятся карта, физика
    def __init__(self):
        self.players = {}

    #передаем подключения игрока входящее и превращаем в игрока
    def add_player(self, client, name):
        self.players[client] = Player(client, name)

    #удаляем по подключению игрока похожего
    def remove_player(self, client):
        if client in self.players:
            del self.players[client]

    #обработка движения на карте
    def handle_move(self, client, x, y):
        #получаем игрока по сходству соединений
        player = self.players.get(client)
        if not player:
            return
        player.x = x
        player.y = y

    #собираем состояние игры для отправки всем подключенным клиентам
    #пока координаты имя здоровье
    def build_state(self):
        state = {
            "players": [
                {"name": p.name, "x": p.x, "y": p.y, "hp": p.hp}
                for p in self.players.values()
            ]
        }
        return create_game_state_message(state)
