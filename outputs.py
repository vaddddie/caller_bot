def get_init_message(message):
    return f'Привет, {message.from_user.first_name}! Я - бот, который с радостью поможет тебе создать группы участников и тегать их одной командой!'

def get_setting_group_message():
    return 'Здесь ты можешь добавлять, изменять и удалять группы участников'

def get_setting_members_message():
    return 'Здесь ты можешь добавлять и удалять участников внутри выбранной группы'

SELECTING_GROUP_MESSAGE = 'Выберите группу..'

ADD_NEW_GROUP_TEXT = 'Добавить новую группу'
CHANGE_GROUP_TEXT = 'Изменить группу'
DELETE_GROUP_TEXT = 'Удалить группу'
HELP_TEXT = 'Помощь'
CHANGE_CHAT_TEXT = 'Изменить выбранный чат'
UNSEEN_TEXT = 'Скрыть'

RENAME_GROUP_TEXT = 'Переименовать группу'
ADD_NEW_MEMBERS_TEXT = 'Добавить новых участников'
DELETE_MEMBERS_TEXT = 'Удалить участников'
BACK_TEXT = 'Назад'






