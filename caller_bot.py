from telebot.async_telebot import AsyncTeleBot
from telebot import types
from db_connector import *
from keyboards import *
from outputs import *
from roadmap_keys import *
from logs import *
import asyncio

test_db_groups = ['qwe', 'reeg', 'errfe']
test_db_members = {
    test_db_groups[0]: ['@fewe', '@ewfwfew', '@ewfe'],
    test_db_groups[1]: ['@hergfwe', '@ewfwfew', '@tyhtyhtye'],
}

test_db_chats = ['-1002052483237', '-4103901665', '-1001676661522']

class caller_bot:
    def __init__(self, token: str) -> None:
        super().__init__()
        self.bot = AsyncTeleBot(token)
        self.listening()

        log_bot_start()
        
        self.test_state = 0
        self.chat_id = 0
        self.group_id = 0

        # /init there
        # .
        # .
        # .
        # /

    def run(self) -> None:
        # Loop
        asyncio.run(self.bot.polling(none_stop=True, interval=0))

    def listening(self) -> None:
        # /Callback handlers initializations there
        # .
        # .
        # .
        # /
        @self.bot.message_handler(commands=['start'], chat_types=['private'])
        async def start_handler(message) -> None:
            # Only private
            # Logs
            log_message_reseived('private', message)
            
            await self.chat_selecting(message.chat.id, message.from_user.id)

        @self.bot.callback_query_handler(func=lambda call:True)
        async def callback_query(call) -> None:
            # Routes

            # GROUPS

            if call.data == ADD_GROUP_CALLBACK:
                await self.group_adding(call.message.chat.id, call.from_user.id)

            if call.data == CHANGE_GROUP_CALLBACK:
                await self.group_changing(call.message.chat.id, call.from_user.id)

            if call.data == DELETE_GROUP_CALLBACK:
                await self.group_deleting(call.message.chat.id, call.from_user.id)

            if call.data == HELP_CALLBACK:
                pass

            if call.data == CHANGE_CHAT_CALLBACK:
                await self.chat_selecting(call.message.chat.id, call.from_user.id)

            if call.data == UNSEEN_CALLBACK:
                pass

            # MEMBERS

            if call.data == RENAME_GROUP_CALLBACK:
                await self.group_renaming(call.message.chat.id, call.from_user.id)

            if call.data == ADD_MEMBERS_CALLBACK:
                await self.member_adding(call.message.chat.id, call.from_user.id)

            if call.data == DELETE_MEMBERS_CALLBACK:
                await self.member_deleting(call.message.chat.id, call.from_user.id)

            if call.data == BACK_CALLBACK:
                # await self.bot.delete_message(call.message.chat.id, call.message.message_id)
                await self.chat_panel_view(call.message)

            await self.bot.delete_message(call.message.chat.id, call.message.message_id)

        @self.bot.message_handler(content_types=['new_chat_members'])
        async def test_func(message) -> None:
            print(message.chat.id)
        # Изменить название функции
        # Настроить внесение в базу данных
        # Сделать проверку айдишника входящего и дополнить функцией выхода

        # Сделать проверку на выходцев из чата чтобы обнулить им чат_айди

        @self.bot.message_handler(content_types='text', chat_types=['private'])
        async def echo_message(message) -> None:
            # Listening other messages

            # Logs
            log_message_reseived('private', message)
            user_state:int = get_user_state(message.from_user.id)

            if user_state == 1:
                await self.chat_selected(message) # Chat selecting
            if user_state == 2:
                if message.text == 'Отмена':
                    set_user_state(message.from_user.id, 0)
                    await self.chat_panel_view(message)
                    return
                await self.group_changed(message) # Group selecting
            if user_state == 3:
                if message.text == 'Отмена':
                    set_user_state(message.from_user.id, 0)
                    await self.chat_panel_view(message)
                    return
                await self.group_added(message) # Group adding
            if user_state == 4:
                if message.text == 'Отмена':
                    set_user_state(message.from_user.id, 0)
                    await self.group_panel_view(message)
                    return
                await self.member_added(message) # Member adding
            if user_state == 5:
                if message.text == 'Отмена':
                    set_user_state(message.from_user.id, 0)
                    await self.chat_panel_view(message)
                    return
                await self.group_deleted(message) # Group deleting
            if user_state == 6:
                if message.text == 'Отмена':
                    set_user_state(message.from_user.id, 0)
                    await self.group_panel_view(message)
                    return
                await self.member_deleted(message) # Member deleting
            if user_state == 7: 
                if message.text == 'Отмена':
                    set_user_state(message.from_user.id, 0)
                    await self.group_panel_view(message)
                    return
                await self.group_renamed(message) # Group renaming

    async def chat_selecting(self, chat_id:int, user_id:int) -> None:
        chats = await self.get_all_chats(user_id)
        
        if len(chats) == 0:
            set_user_state(user_id, 0)
            await self.bot.send_message(chat_id, 'Для начала пригласи бота в чат, в котором ты являешься администратором')
            return
        
        chats_titles = chats.keys()

        set_user_state(user_id, 1)
        await self.bot.send_message(chat_id, 'Выбери чат для редактирования..', reply_markup=get_reply_keyboard(chats_titles, cancel=False))
        return

    async def chat_selected(self, message:types.Message) -> None:
        set_user_state(message.from_user.id, 0)
        chats = await self.get_all_chats(message.from_user.id)
        
        try:
            set_user_chat(message.from_user.id, chats[message.text])
            chat_title = message.text
        except:
            await self.bot.send_message(message.chat.id, 'Ошибка, попробуй ещё раз..')
            await self.chat_selecting(message.chat.id, message.from_user.id)
            return

        await self.bot.send_message(message.chat.id, f'Выбран чат \"{chat_title}\"', reply_markup=types.ReplyKeyboardRemove())
        await self.chat_panel_view(message)
        return

    async def group_adding(self, chat_id:int, user_id:int)-> None:
        set_user_state(user_id, 3)
        await self.bot.send_message(chat_id, 'Напишите название новой группы', reply_markup=get_reply_keyboard())
        return

    async def group_added(self, message:types.Message) -> None:
        set_user_state(message.from_user.id, 0)
        
        if not create_new_group(get_user_chat(message.from_user.id), message.text):
            await self.bot.send_message(message.chat.id, 'Ошибка, попробуй ещё раз..')
            await self.group_adding(message.chat.id, message.from_user.id)
            return

        set_user_group(message.from_user.id, message.text)
        
        await self.bot.send_message(message.chat.id, f'Создана группа {message.text}', reply_markup=types.ReplyKeyboardRemove())
        await self.group_panel_view(message)
        return

    async def group_changing(self, chat_id:int, user_id:int) -> None:
        set_user_state(user_id, 2)

        await self.bot.send_message(chat_id, 'Выберите группу', reply_markup=get_reply_keyboard(get_groups_by_idChat(get_user_chat(user_id))))
        return

    async def group_changed(self, message:types.Message) -> None:
        set_user_state(message.from_user.id, 0)

        if message.text not in get_groups_by_idChat(get_user_chat(message.from_user.id)):
            await self.bot.send_message(message.chat.id, 'Ошибка, попробуйте ещё раз..')
            await self.group_changing(message.chat.id, message.from_user.id)
            return

        set_user_group(message.from_user.id, message.text)
        await self.bot.send_message(message.chat.id, f'Выбрана группа {message.text}', reply_markup=types.ReplyKeyboardRemove())
        await self.group_panel_view(message)
        return

    async def group_deleting(self, chat_id:int, user_id:int) -> None:
        set_user_state(user_id, 5)

        await self.bot.send_message(chat_id, 'Выберите группу', reply_markup=get_reply_keyboard(get_groups_by_idChat(get_user_chat(user_id))))  
        return      

    async def group_deleted(self, message:types.Message) -> None:
        set_user_state(message.from_user.id, 0)

        if message.text not in get_groups_by_idChat(get_user_chat(message.from_user.id)):
            await self.bot.send_message(message.chat.id, 'Ошибка, попробуйте ещё раз..')
        else:
            await self.bot.send_message(message.chat.id, f'Группа {message.text} удалена', reply_markup=types.ReplyKeyboardRemove())
            delete_group(get_user_chat(message.from_user.id), message.text)
            
        await self.group_deleting(message.chat.id, message.from_user.id)
        return

    async def chat_panel_view(self, message:types.Message) -> None:
        await self.bot.send_message(message.chat.id, get_init_message(message), reply_markup=get_inline_keyboard('chat'))
        return

    async def group_panel_view(self, message:types.Message) -> None:
        await self.bot.send_message(message.chat.id, get_init_message(message), reply_markup=get_inline_keyboard('group'))
        return




    async def group_renaming(self, chat_id:int, user_id:int) -> None:
        set_user_state(user_id, 7)

        await self.bot.send_message(chat_id, 'Введите новое название группы', reply_markup=get_reply_keyboard())
        return

    async def group_renamed(self, message:types.Message) -> None:
        set_user_state(message.from_user.id, 0)

        rename_group(get_user_group(message.from_user.id), message.text)

        await self.bot.send_message(message.chat.id, f'Группа переименована', reply_markup=types.ReplyKeyboardRemove())
        await self.group_panel_view(message)
        return

    async def member_adding(self, chat_id:int, user_id:int) -> None:
        set_user_state(user_id, 4)

        await self.bot.send_message(chat_id, f'Введите новых пользователей', reply_markup=get_reply_keyboard())
        return

    async def member_added(self, message:types.Message) -> None:
        set_user_state(message.from_user.id, 0)

        members = message.text.split()
        
        for i in range(len(members)):
            if members[i][0] != '@':
                members[i] = '@' + members[i]
            # if members[i] in get_all_members_by_idGroup(get_user_group(message.from_user.id)):
            #     members.pop(i)

        add_members(get_user_group(message.from_user.id), members)

        await self.bot.send_message(message.chat.id, f'Пользователи добавлены', reply_markup=types.ReplyKeyboardRemove())
        await self.member_adding(message.chat.id, message.from_user.id)
        return

    async def member_deleting(self, chat_id:int, user_id:int) -> None:
        set_user_state(user_id, 6)

        await self.bot.send_message(chat_id, f'Выберете удалаемых пользователей', reply_markup=get_reply_keyboard(get_all_members_by_idGroup(get_user_group(user_id))))
        return

    async def member_deleted(self, message:types.Message) -> None:
        set_user_state(message.from_user.id, 0)

        if message.text not in get_all_members_by_idGroup(get_user_group(message.from_user.id)):
            await self.bot.send_message(message.chat.id, 'Ошибка, попробуйте ещё раз..')
        else:
            delete_member(get_user_group(message.from_user.id), message.text)
            await self.bot.send_message(message.chat.id, f'Участники {message.text} удалены', reply_markup=types.ReplyKeyboardRemove())

        await self.member_deleting(message.chat.id, message.from_user.id)
        return

    async def get_all_chats(self, user_id:int):
        chats = {}

        for idChat in get_all_idChats():
            try:
                chat_id = idChat_2_chat_id(idChat)
                member = await self.bot.get_chat_member(chat_id, user_id)
                if member.status != 'member':
                    title = (await self.bot.get_chat(int(chat_id))).title
                    chats[title] = idChat
            except:
                pass
        
        return chats
