import pickle

# типы сообщений на наличие которого мы будем проверять
MESSAGE_TYPES = {
    "signup",
    "move",
    "shot",
    "game_state",
    "chat",
    "exit_game"
}

# проверка является ли сообщение словарем и содержит ли 
# тип из массива
def validate(message):
    if isinstance(message, dict) and message["type"] in MESSAGE_TYPES:
        return True
    return False

# преобразование сообщения в байты для отправки по сети
def serialize_message(message):
    if not validate(message):
        raise ValueError(f"Неверный формат сообщения {message}")
    return pickle.dumps(message)

def deseralize_message(data):
    message = pickle.loads(data)
    if not validate(message):
        raise ValueError(f"Неверный формат сообщения {message}")
    return message

def create_signup_message(name):
    return {"type": "signup", "name": name}

def create_move_message(x, y):
    return {"type": "move", "x": x, "y": y}

def create_shot_message(angle, power):
    return {"type": "shot", "angle": angle, "power": power}

def create_game_state_message(state):
    return {"type": "game_state", "state": state}

def create_chat_message(text):
    return {"type": "chat", "text": text}

def create_exit_message():
    return {"type": "exit_game"}