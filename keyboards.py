from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from outputs import *
from roadmap_keys import *

test_db_groups = ['qwe', 'reeg', 'errfe']
test_db_members = {
    test_db_groups[0]: ['@fewe', '@ewfwfew', '@ewfe'],
    test_db_groups[1]: ['@hergfwe', '@ewfwfew', '@tyhtyhtye'],
}

def get_reply_keyboard(items: list=[], cancel:bool=True) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(one_time_keyboard=False)

    if cancel: markup.add(KeyboardButton('Отмена'))
    for item in items:
        item_button = KeyboardButton(item)
        markup.add(item_button)

    return markup

def get_group_selecting_keyboard() -> ReplyKeyboardMarkup:
    return 

def get_inline_keyboard(type: str) -> InlineKeyboardMarkup:
    if type == 'chat':
        markup = InlineKeyboardMarkup(row_width=2)

        button_add_group = InlineKeyboardButton(ADD_NEW_GROUP_TEXT, callback_data=ADD_GROUP_CALLBACK)
        button_change_group = InlineKeyboardButton(CHANGE_GROUP_TEXT, callback_data=CHANGE_GROUP_CALLBACK)
        button_delete_group = InlineKeyboardButton(DELETE_GROUP_TEXT, callback_data=DELETE_GROUP_CALLBACK)
        button_help = InlineKeyboardButton(HELP_TEXT, callback_data=HELP_CALLBACK)
        button_change_chat = InlineKeyboardButton(CHANGE_CHAT_TEXT, callback_data=CHANGE_CHAT_CALLBACK)
        button_unseen = InlineKeyboardButton(UNSEEN_TEXT, callback_data=UNSEEN_CALLBACK)

        markup.add(button_add_group)
        markup.add(button_change_group)
        markup.add(button_delete_group)
        markup.add(button_help)
        markup.add(button_change_chat)
        markup.add(button_unseen)

        return markup

    if type == 'group':
        markup = InlineKeyboardMarkup()

        button_rename_group = InlineKeyboardButton(RENAME_GROUP_TEXT, callback_data=RENAME_GROUP_CALLBACK)
        button_add_member = InlineKeyboardButton(ADD_NEW_MEMBERS_TEXT, callback_data=ADD_MEMBERS_CALLBACK)
        button_delete_member = InlineKeyboardButton(DELETE_MEMBERS_TEXT, callback_data=DELETE_MEMBERS_CALLBACK)
        button_back = InlineKeyboardButton(BACK_TEXT, callback_data=BACK_CALLBACK)

        markup.add(button_rename_group)
        markup.add(button_add_member)
        markup.add(button_delete_member)
        markup.add(button_back)

        return markup

