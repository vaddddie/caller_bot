from telebot import types
from datetime import datetime


def get_datetime_now() -> str:
    now = datetime.now()
    current_time = now.strftime('%d.%m.%y %H:%M:%S')
    
    return current_time

def log_bot_start() -> None:
    print(f'[{get_datetime_now()}] Launching the bot')
    
def log_message_reseived(type: str, message: types.Message) -> None:
    if type == 'private':
        print(f'[{get_datetime_now()}] A private message has been received\n |-| from user: \"{message.from_user.first_name}\".\n |-| Message: \"{message.text}\".')
    if type == 'group':
        print(f'[{get_datetime_now()}] A message was received\n |-| from a user: \"{message.from_user.first_name}\"\n |-| in the \"{message.chat.title}\" chat.\n |-| Message: \"{message.text}\".')

def log_connecting_to_db() -> None:
    print(f'[{get_datetime_now()}] Attempting to connect to the datebase..')

def log_connected_to_db() -> None:
    print(f'[{get_datetime_now()}] The database is connected.')

def log_error_connection_to_db() -> None:
    print(f'[{get_datetime_now()}] Database connection error')

def log_new_user(user_id:int) -> None:
    print(f'[{get_datetime_now()}] A new user has been added.\n |-| User_id: {user_id}')