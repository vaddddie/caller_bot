import mysql.connector
from logs import log_connecting_to_db, log_connected_to_db, log_error_connection_to_db, log_new_user

conn = None

def connect_to_db(attempts=3) -> None:
    global conn

    config = {
        "host": "127.0.0.1",
        "user": "caller_bot",
        "password": "password",
        "database": "caller_bot_db",
    }

    for i in range(attempts):
        log_connecting_to_db()
        try:
            conn = mysql.connector.connect(**config)
            log_connected_to_db()
            break
        except:
            log_error_connection_to_db()
    return

def sql_exec(cmd:str) -> []:
    if conn == None or not conn.is_connected(): connect_to_db()

    with conn.cursor() as cursor:
        cursor.execute(cmd)
        result = cursor.fetchall()

    return result

def sql_commit(cmd:str) -> None:
    if conn == None or not conn.is_connected(): connect_to_db()

    with conn.cursor() as cursor:
        cursor.execute(cmd)
        conn.commit()

    return

def check_user(user_id:int) -> None:
    result = sql_exec(f'SELECT * FROM `User` WHERE `user_id` = {user_id} LIMIT 1;')
    if result == []: 
        sql_commit(f'INSERT INTO `User`(`user_id`) VALUES (\'{user_id}\');')
        log_new_user(user_id)

    return

def get_user_state(user_id:int) -> int:
    check_user(user_id)
    result = sql_exec(f'SELECT `state` FROM `User` WHERE `user_id` = {user_id} LIMIT 1;')

    return result[0][0]

def set_user_state(user_id:int, state:int) -> None:
    check_user(user_id)
    sql_commit(f'UPDATE `User` SET `state` = {state} WHERE `user_id` = {user_id};')

    return

def idChat_2_chat_id(idChat:int) -> str:
    result = sql_exec(f'SELECT `chat_id` FROM `Chat` WHERE `idChat` = \'{idChat}\' LIMIT 1;')
    return result[0][0]

def get_all_idChats() -> []:
    tmp = sql_exec(f'SELECT `idChat` FROM `Chat`;')

    result = []
    for item in tmp:
        result.append(str(item[0]))

    return result

def get_user_chat(user_id:int) -> int:
    check_user(user_id)
    result = sql_exec(f'SELECT `idChat` FROM `User` WHERE `user_id` = \'{user_id}\' LIMIT 1;')
    if result == []: return None
    return str(result[0][0])

def set_user_chat(user_id:int, idChat:int) -> None:
    check_user(user_id)
    sql_commit(f'UPDATE `User` SET `idChat` = \'{idChat}\', `idGroup` = NULL WHERE `user_id` = {user_id};')
    return

def get_user_group(user_id:int) -> int:
    check_user(user_id)
    result = sql_exec(f'SELECT `idGroup` FROM `User` WHERE `user_id` = {user_id} LIMIT 1;')
    if result == []: return None
    return result[0][0]

def set_user_group(user_id:int, group_title:str) -> None:
    check_user(user_id)
    idChat:int = get_user_chat(user_id)
    sql_commit(f'UPDATE `User` SET `idGroup` = (SELECT `idGroup` FROM `Group` WHERE `idChat` = \'{idChat}\' AND `group_title` = \'{group_title}\' LIMIT 1) WHERE `user_id` = \'{user_id}\' LIMIT 1;')
    return

def create_new_group(idChat:int, title:str) -> bool:
    try:
        sql_commit(f'INSERT INTO `Group`(`idChat`, `group_title`) VALUES(\'{idChat}\', \'{title}\');')
        return True
    except:
        return False

def get_groups_by_idChat(idChat:int) -> []:
    tmp = sql_exec(f'SELECT `group_title` FROM `Group` WHERE `idChat` = \'{idChat}\';')
    
    result = [item[0] for item in tmp]

    return result

def delete_group(idChat:int, group_title:str) -> None:
    sql_commit(f'DELETE FROM `Group` WHERE `idChat` = \'{idChat}\' AND `group_title` = \'{group_title}\';')
    return

def rename_group(idGroup:int, new_group_title:str) -> None:
    sql_commit(f'UPDATE `Group` SET `group_title` = \'{new_group_title}\' WHERE `idGroup` = \'{idGroup}\';')
    return

def add_members(idGroup:int, members:[]) -> None:
    for item in members:
        sql_commit(f'INSERT INTO `Member`(`idGroup`, `member_title`) VALUES (\'{idGroup}\', \'{item}\');')
    return

def get_all_members_by_idGroup(idGroup:int) -> []:
    tmp = sql_exec(f'SELECT `member_title` FROM `Member` WHERE `idGroup` = \'{idGroup}\';')

    result = [item[0] for item in tmp]

    return result

def delete_member(idGroup:int, member_title:str) -> None:
    sql_commit(f'DELETE FROM `Member` WHERE `idGroup` = \'{idGroup}\' AND `member_title` = \'{member_title}\';')
    return


