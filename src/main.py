from commands import *

init_db()


# КОМАНДЫ
@bot.message_handler(commands=["start", "chat_id", "admin", "send", "show_users", "add_pay_basic", "add_pay_hrplus", "send_info_all_users", "discount_yes", "discount_no", "send_show_post"])
def start_handler(message):
    user_id, chat_id, username = get_easy_message(message)
    add_user_status(user_id, "")

    if len(message.text.split()) > 1 and message.text.split()[1] == 'post':
        post(message)
    elif message.text == "/start":
        start(message)
    elif message.text == "/chat_id":
        bot.send_message(chat_id, chat_id)

    #Админские команды
    if str(chat_id) == ADMIN_ID:
        if message.text == "/admin":
            admin(message)
        elif message.text == "/send":
            send()
        elif message.text == "/send_show_post":
            send_show_post()
        elif message.text == "/show_users":
            show_users(message)
        elif message.text == "/add_pay_basic":
            add_pay_basic(message)
        elif message.text == "/add_pay_hrplus":
            add_pay_hrplus(message)
        elif message.text == "/send_info_all_users":
            send_info_all_users(message)
        elif message.text == '/discount_yes':
            dicount_yes(message)
        elif message.text == '/discount_no':
            dicount_no(message)

# CALLBACK
@bot.callback_query_handler(func=lambda call: call.data in CALLBACK)
def callback_handler(callback):
    answer = callback.data

    # ОБРАБОТКА РАЗНЫХ ОТВЕТОВ
    if answer == "help":
        callback_help(callback)
    elif answer == "back_to_main_menu":
        callback_main_menu(callback)
    elif answer in ["profile", "before_post", "next_post"]:
        callback_my_posts(callback)
    elif answer in ["send_post", "redact"]:
        callback_send_redact_post(callback)
    elif answer == "moderation":
        callback_moderation(callback)
    elif answer in ["pay_basic", "pay_premium", "pay_hrplus"]:
        process_payment(callback)
    elif answer == "check_payment":
        check_payment_handler(callback)

@bot.callback_query_handler(func=lambda call: call.data.startswith("approve_") or call.data.startswith("reject_") or call.data.startswith("rpost_"))
def approve_post(callback):
    if callback.data.startswith("approve_"):
        approve(callback)
    elif callback.data.startswith("reject_"):
        reject(callback)
    elif callback.data.startswith("rpost_"):
        rpost(callback)

# ТЕКСТ
@bot.message_handler(func=lambda message: message.text == "📋 ГЛАВНОЕ МЕНЮ")
def back_to_main_menu_handler(message):
    user_id, chat_id, username = get_easy_message(message)

    # Удаление предыдущего сообщения
    if message.text == "📋 ГЛАВНОЕ МЕНЮ":
        delete_message_plus(user_id, chat_id)

        # Статус = None
        add_user_status(user_id, "")

        # Отправка главного меню
        sent_message = bot.send_message(
            chat_id,
            welcome_text(user_id),
            reply_markup=main_menu_buttons(), parse_mode="Markdown"  # Inline-клавиатура главного меню
        )

        # Сохраняем ID сообщения для последующего удаления
        add_delete_message_id(user_id, sent_message.message_id)

# СТАТУСЫ
@bot.message_handler(func=lambda message: get_user_status(message.from_user.id) in ["waiting_for_post", "waiting_nick_basic", "waiting_nick_hr", "waiting_message_to_sand"] or get_user_status(message.from_user.id).startswith("waiting_reason_") or get_user_status(message.from_user.id).startswith("waiting_redact_"))
def status_hendler(message):
    user_id, chat_id, username = get_easy_message(message)

    status = get_user_status(user_id)

    # Статус ожидания поста
    if status == "waiting_for_post":
        # Удаление предыдущего сообщения
        delete_message_one(user_id, chat_id)

        # Отправка сообщения и Добавления id сообщения в бд
        sent_message = bot.send_message(
            message.chat.id,
            f"✅ *Предварительный просмотр:*\n\n————————————\n{message.text}\n————————————\n\n*Всё верно?*",
            reply_markup=redact_button(),
            parse_mode="Markdown",
        )
        add_delete_message_id(user_id, sent_message.message_id)

        # Нулевой статус
        add_user_status(user_id, "")
        add_save_post(user_id, message.text)

    if status.startswith("waiting_reason_"):
        post_id = int(status.split("_")[2])
        post_data = get_post_data(post_id)

        if post_data:
            author_id = post_data["user_id"]
            content = post_data["content"]

            delete_message_one(author_id, get_chat_id(author_id))

            # Отправляем уведомление автору
            text = (
                "😔 К сожалению, ваше объявление *не прошло модерацию*.\n\n"
                "📋 *Причина отклонения:*\n"
                f"_{message.text}_\n\n"
                "🛠 *Как исправить:*\n"
                "1. Перейдите в раздел «📊 МОИ ПОСТЫ»\n"
                "2. Нажмите кнопку «✏️ РЕДАКТИРОВАТЬ»\n"
                "3. Внесите необходимые правки\n"
                "4. Отправьте исправленный вариант\n\n"
            )
            sent_message = bot.send_message(
                author_id, text, reply_markup=my_posts_buttons(), parse_mode="Markdown"
            )

            add_user_status(user_id, "")
            add_delete_message_id(author_id, sent_message.message_id)

            bot.send_message(
                chat_id, f"✅ Причина отклонения отправлена автору поста #{post_id}\n---------------------------\n{content}\n---------------------------"
            )
        else:
            bot.send_message(chat_id, "❌ Ошибка: пост не найден")
            add_user_status(user_id, "")

    if status == "waiting_nick_basic":
        users = get_all_users()
        flag = False
        for user in users:
            if message.text == user['username']:
                true_user = user
                flag = True
                break
        if flag:
            activate_tariff(true_user['user_id'], 'pay_basic')
            bot.send_message(chat_id, f"пользователю @{true_user['username']}, добавлен 1 бесплатный пост")

        else:
            bot.send_message(chat_id, "Такого пользователя нет")

        add_user_status(user_id, "")

    if status == "waiting_nick_hr":
        users = get_all_users()
        flag = False
        for user in users:
            if message.text == user['username']:
                true_user = user
                flag = True
                break
        if flag:
            activate_tariff(true_user['user_id'], 'pay_hrplus')
            bot.send_message(chat_id, f"пользователю @{true_user['username']}, добавлена подписка на 30 дней")

        else:
            bot.send_message(chat_id, "Такого пользователя нет")

        add_user_status(user_id, "")

    if status.startswith("waiting_redact_"):
        post_id = int(status.split("_")[2])
        post_data = get_post_data(post_id)
        if post_data:
            author_id = post_data["user_id"]

            add_approval_status(post_id, '🕐 На модерации')
            add_content(post_id, message.text)

            delete_message_one(author_id, get_chat_id(author_id))

            sent_message = bot.send_message(chat_id, text=moderation_text(), reply_markup=main_menu_buttons(), parse_mode="Markdown")

            add_delete_message_id(author_id, sent_message.message_id)

            send_post_to_admins(post_id, message.text, username, "Повторный пост")

            add_user_status(user_id, "")

    if status == "waiting_message_to_sand":
        users = get_all_users()
        if message.text != "Отмена":
            for user in users:
                bot.send_message(user['chat_id'], message.text)
        add_user_status(user_id, "")


bot.polling()
