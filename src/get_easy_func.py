from buttoms import *


## Упрощающие функции
def get_easy_message(message):
    return message.from_user.id, message.chat.id, message.from_user.username


def get_easy_callback(callback):
    return callback.from_user.id, callback.message.chat.id, callback.message.id


# Удаление сообщения
def delete_message_one(user_id, chat_id):
    delete_message = get_delete_message_id(user_id)
    if delete_message is not None:
        try:
            bot.delete_message(chat_id, delete_message)
        except Exception as e:
            # Игнорируем ошибку "message not found"
            if "message to delete not found" not in str(e):
                print(f"Ошибка при удалении сообщения: {e}")

def delete_message_minus(user_id, chat_id):
    delete_message = get_delete_message_id(user_id)
    if delete_message is not None:
        try:
            bot.delete_message(chat_id, delete_message)
            bot.delete_message(chat_id, delete_message - 1)
        except Exception as e:
            # Игнорируем ошибку "message not found"
            if "message to delete not found" not in str(e):
                print(f"Ошибка при удалении сообщения: {e}")


def delete_message_plus(user_id, chat_id):
    delete_message = get_delete_message_id(user_id)
    if delete_message != None:
        try:
            # Удаляем каждое сообщение отдельно
            bot.delete_message(chat_id, delete_message)
            bot.delete_message(chat_id, delete_message + 1)
        except Exception as e:
            # Игнорируем ошибки если сообщения уже удалены
            print(f"Ошибка при удалении сообщения: {e}")

#Двойная проверка перед изменением
def edit_message_text_hendler(**kwargs):
    try:
        bot.edit_message_text(**kwargs)
    except Exception as e:
        error_msg = str(e)
        
        # Игнорируем ошибку "message is not modified"
        if "message is not modified" in error_msg:
            print("Сообщение не требует изменений - пропускаем")
            return
        # Игнорируем ошибку "query is too old"
        elif "query is too old" in error_msg:
            print("Callback устарел - пропускаем")
            return
        else:
            print(f"Ошибка при изменении сообщения: {e}")
            # Повторная попытка только для других ошибок
            try:
                time.sleep(1)
                bot.edit_message_text(**kwargs)
            except Exception as e2:
                print(f"Повторная попытка также не удалась: {e2}")