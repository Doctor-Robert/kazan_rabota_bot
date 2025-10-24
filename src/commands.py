from callback import *

def post(message):
    user_id, chat_id, username = get_easy_message(message)
    add_user_and_nickname(user_id, username, chat_id)
    # Если перешли по кнопке из группы
    delete_message_minus(user_id, chat_id)
    text = (
        "👋 *Добро пожаловать в главный бот по работе в Казани!* 💼\n\n"
        "📝 *Давайте создадим ваше первое объявление!*\n\n"
        "• *Заголовок* (например: \"Срочно требуются грузчики на склад\")\n"
        "• *Подробное описание*: задачи, условия, требования\n"
        "• *Условия оплаты*: \"2000 руб/смена\", \"договорная\", \"почасовая\"\n"
        "• *Контакты*: телефон, Telegram для связи\n\n"
        "📨 *Отправьте мне пост одним сообщением* 👇"
    )
    add_user_status(user_id, "waiting_for_post")
    sent_message = bot.send_message(message.chat.id, text, reply_markup=back_to_main_menu_button_reply(), parse_mode='Markdown')
    add_delete_message_id(user_id, sent_message.message_id)

def start(message):
    user_id, chat_id, username = get_easy_message(message)

    add_user_and_nickname(user_id, username, chat_id)

    # Удаление сообщения
    delete_message_minus(user_id, chat_id)

    # Отправка сообщения и Добавления id сообщения в бд
    sent_message = bot.send_message(
        chat_id, welcome_text(user_id), reply_markup=main_menu_buttons(), parse_mode="Markdown"
    )
    add_delete_message_id(user_id, sent_message.message_id)



#Админские команды
def admin(message):
    user_id, chat_id, username = get_easy_message(message)
    bot.send_message(chat_id, admin_comands())

def send():
    kb = types.InlineKeyboardMarkup()
    btm1 = types.InlineKeyboardButton("📤 Разместить объявление", url="https://t.me/Gruzchik_Kazan_bot?start=post")
    kb.add(btm1)
    text = "🤝 ИЩЕШЬ РАБОТУ ИЛИ РАБОТНИКОВ?\n\nНажмите кнопку ниже, чтобы быстро разместить своё объявление в нашем боте! 👇\n\n@KazanRabotaa_bot"
    bot.send_message(ADMIN_ID, "Сообщение отправлено")
    for i in range(len(GROUP_CHAT_ID)):
        try:
            bot.send_message(GROUP_CHAT_ID[i], text, reply_markup=kb)
        except:
            print("false")

def send_show_post():
    kb = types.InlineKeyboardMarkup()
    btm1 = types.InlineKeyboardButton("📤 Разместить объявление", url="https://t.me/Gruzchik_Kazan_bot?start=post")
    kb.add(btm1)
    text = (
        "🎉 <b>ЗАПУСКАЕМ ОБНОВЛЕННЫЙ БОТ ДЛЯ РАБОТЫ В КАЗАНИ!</b> 🚀\n\n"
        
        "🔥 <b>СКИДКА 50% НА ВСЕ ТАРИФЫ</b>\n"
        "Только сегодня! Успей разместить объявление по специальной цене\n\n"
        
        "⚡ <b>ПРЕИМУЩЕСТВА:</b>\n"
        "• Мгновенная публикация\n"
        "• Прямой контакт с исполнителями\n" 
        "• Точный подбор по сфере\n"
        "• Приоритет для первых 100 пользователей\n\n"
        
        "⏰ <b>АКЦИЯ ДЕЙСТВУЕТ ТОЛЬКО СЕГОДНЯ!</b>\n\n"
        
        "👇 <b>Нажми кнопку и начни получать отклики:</b>\n"
        "@KazanRabotaa_bot"
    )
    bot.send_message(ADMIN_ID, "Сообщение отправлено")

    for i in range(len(GROUP_CHAT_ID)):
        try:
            bot.send_message(GROUP_CHAT_ID[i], text, reply_markup=kb, parse_mode='HTML')
        except:
            print("false")

def show_users(message):
    users = get_all_users()
    response = f"📊 Список пользователей (всего: {len(users)}):\n\n"

    for user in users:
        response += f"👤@{user['username'] or 'нет'}\n"
    
    try:
        bot.send_message(message.chat.id, response)
    except Exception as e:
        bot.send_message(message.chat.id, f"Сообщение слишком большое, число пользователей = {len(users)}")

def add_pay_basic(message):
    user_id, chat_id, username = get_easy_message(message)

    bot.send_message(chat_id, "Введите Никнэйм:")
    add_user_status(user_id, "waiting_nick_basic")

def add_pay_hrplus(message):
    user_id, chat_id, username = get_easy_message(message)

    bot.send_message(chat_id, "Введите Никнэйм:")
    add_user_status(user_id, "waiting_nick_hr")

def send_info_all_users(message):
    user_id, chat_id, username = get_easy_message(message)

    bot.send_message(chat_id, "Введите сообщение для отправки людям:\n\nили напишите 'Отмена'")
    add_user_status(user_id, "waiting_message_to_sand")

def dicount_yes(message):
    user_id, chat_id, username = get_easy_message(message)
    users = get_all_users()
    for user in users:
        add_discount(user["user_id"], 'yes')

    bot.send_message(chat_id, "Скидка 50% активирована")

def dicount_no(message):
    user_id, chat_id, username = get_easy_message(message)
    users = get_all_users()
    for user in users:
        add_discount(user["user_id"], 'no')

    bot.send_message(chat_id, "Скидка 50% отменена")

