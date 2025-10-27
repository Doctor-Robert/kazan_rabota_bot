from payment import *

num_post = 0
    
#Помощь
def callback_help(callback):
    try:
        bot.answer_callback_query(callback.id)
    except Exception as e:
        print(f"Ошибка ответа на callback: {e}")

    user_id, chat_id, message_id = get_easy_callback(callback)
    edit_message_text_hendler(chat_id=chat_id, message_id=message_id, text=help_text(), reply_markup=back_to_main_menu_button(), parse_mode="Markdown")

#Главное меню
def callback_main_menu(callback):
    try:
        bot.answer_callback_query(callback.id)
    except Exception as e:
        # Игнорируем ошибки устаревших callback
        if "query is too old" not in str(e):
            print(f"Ошибка ответа на callback: {e}")

    user_id, chat_id, message_id = get_easy_callback(callback)
    add_user_status(user_id, "")
    
    try:
        edit_message_text_hendler(
            chat_id=chat_id, 
            message_id=message_id, 
            text=welcome_text(user_id), 
            reply_markup=main_menu_buttons(), 
            parse_mode="Markdown"
        )
    except Exception as e:
        print(f"Ошибка в callback_main_menu: {e}")

# Мои посты
def callback_my_posts(callback):
    try:
        bot.answer_callback_query(callback.id)
    except Exception as e:
        print(f"Ошибка ответа на callback: {e}")

    global num_post
    user_id, chat_id, message_id = get_easy_callback(callback)

    add_user_status(user_id, "")

    posts = get_all_posts(user_id)
    if callback.data == 'profile':
        num_post = 0
    elif callback.data == 'before_post':
        num_post += 1
    elif callback.data == 'next_post':
        num_post -= 1

    lenn = len(posts)

    if lenn <= 0:
        kb = back_to_main_menu_button()
    elif num_post == 0 and lenn == 1:
        if posts[num_post]['approval_status'] == "❌ Отклонено":
            post_id = posts[num_post]['post_id']
            kb = back_to_main_menu_change_button(post_id)
        else:
            kb = back_to_main_menu_button()
    elif num_post == 0 and lenn > 1:
        if posts[num_post]['approval_status'] == "❌ Отклонено":
            post_id = posts[num_post]['post_id']
            kb = before_post_change_button(post_id)
        else:
            kb = before_post_button()
    elif num_post + 1 >= lenn:
        if posts[num_post]['approval_status'] == "❌ Отклонено":
            post_id = posts[num_post]['post_id']
            kb = next_post_change_button(post_id)
        else:
            kb = next_post_button()
    else:
        if posts[num_post]['approval_status'] == "❌ Отклонено":
            post_id = posts[num_post]['post_id']
            kb = before_and_next_post_change_button(post_id)
        else:
            kb = before_and_next_post_button()

    if lenn <= 0:
        text = no_post()
    else:
        text = f"📋 *Ваше объявление:*\n\n{posts[num_post]['content']}\n\n*Статус:* {posts[num_post]['approval_status']}"

    try:
        current_message = bot.get_message(chat_id, message_id)
        new_text = text  # ваш новый текст
        new_markup = kb  # ваша новая клавиатура
        
        # Проверяем, действительно ли нужно менять сообщение
        if (current_message.text != new_text or 
            str(current_message.reply_markup) != str(new_markup)):
            edit_message_text_hendler(
                chat_id=chat_id, 
                message_id=message_id, 
                text=new_text, 
                reply_markup=new_markup, 
                parse_mode="Markdown"
            )
    except Exception as e:
        # Если не получается проверить, просто пытаемся изменить
        edit_message_text_hendler(
            chat_id=chat_id, 
            message_id=message_id, 
            text=text, 
            reply_markup=kb, 
            parse_mode="Markdown"
        )

#Выложить пост или редактировать
def callback_send_redact_post(callback):
    try:
        bot.answer_callback_query(callback.id)
    except Exception as e:
        print(f"Ошибка ответа на callback: {e}")

    user_id, chat_id, message_id = get_easy_callback(callback)
    delete_message_one(user_id, chat_id)

    add_user_status(user_id, "waiting_for_post")

    #Отправка сообщения и Добавления id сообщения в бд
    sent_message = bot.send_message(chat_id, after_send_post_text(), reply_markup=back_to_main_menu_button_reply(), parse_mode="Markdown")
    add_delete_message_id(user_id, sent_message.message_id)

#Оплата поста
def callback_moderation(callback):
    try:
        bot.answer_callback_query(callback.id)
    except Exception as e:
        print(f"Ошибка ответа на callback: {e}")

    user_id, chat_id, message_id = get_easy_callback(callback)

    # Проверяем наличие активного тарифа
    posts_available = get_posts_available(user_id)
    expires_at = get_expires_at(user_id)

    posts = get_all_posts(user_id)

    count = 0
    for post in posts:
        if post["approval_status"] == "🕐 На модерации":
            count +=1

    if count >= 3:
        edit_message_text_hendler(chat_id=chat_id, message_id=message_id, text=text_limit_posts(), reply_markup=back_to_main_menu_button(), parse_mode="HTML")

    else:

        if posts_available <= 0:
            if (expires_at == None or datetime.now() > datetime.fromisoformat(expires_at)):
                edit_message_text_hendler(chat_id=chat_id, message_id=message_id, text=text_pay(get_discount(user_id)), reply_markup=pay_button(user_id), parse_mode="HTML")
            else:
                # Если есть активный тариф - сразу отправляем на модерацию
                edit_message_text_hendler(chat_id=chat_id, message_id=message_id, text=moderation_text(), reply_markup=main_menu_buttons(), parse_mode="Markdown")
                post = get_save_post(user_id)
                add_post(user_id, post, callback.from_user.username, "Подписка 30 дней")
        else:
            # Если есть активный тариф - сразу отправляем на модерацию
            edit_message_text_hendler(chat_id=chat_id, message_id=message_id, text=moderation_text(), reply_markup=main_menu_buttons(), parse_mode="Markdown")
            post = get_save_post(user_id)
            add_post(user_id, post, callback.from_user.username, "1 пост")
            add_posts_available(user_id, posts_available - 1)

#Создание Оплаты
def process_payment(callback):
    try:
        bot.answer_callback_query(callback.id)
    except Exception as e:
        print(f"Ошибка ответа на callback: {e}")

    """Обработка выбора тарифа и создание платежа"""
    user_id, chat_id, message_id = get_easy_callback(callback)

    if get_discount(user_id) == "yes":
        tariff_info = TARIFFS_DISCOUNT_50[callback.data]
    else:
        tariff_info = TARIFFS[callback.data]
    
    try:
        # Создаем платеж в ЮKassa
        payment = create_payment_link(
            user_id=user_id,
            tariff_type=callback.data,
            amount=tariff_info['amount'],
            description=f"Тариф {tariff_info['label']}"
        )
        
        # Сохраняем в БД
        create_payment(user_id, payment.id, callback.data, tariff_info['amount'])
        
        
        payment_message = (
            f"💳 *ОПЛАТА ТАРИФА {tariff_info['label']}*\n\n"
            f"💰 Сумма: {tariff_info['amount']} ₽\n\n"
            f"*Инструкция:*\n"
            f"1. Нажмите '💳 Перейти к оплате'\n"
            f"2. Оплатите счет\n"
            f"3. Вернитесь в бот\n\n"
            f"✅ После оплаты пост автоматически отправится на проверку\n"
            f"⏱️ Обычно модерация занимает 2-3 минуты"
        )
        
        edit_message_text_hendler(
            text=payment_message,
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=payment_button(payment.confirmation.confirmation_url),
            parse_mode="Markdown"
        )
        
        # Запускаем автоматическую проверку статуса
        start_payment_checking(payment.id, chat_id, message_id, user_id, callback.data, callback.from_user.username)
        
    except Exception as e:
        error_message = (
            "❌ *Ошибка при создании платежа*\n\n"
            "Попробуйте позже или обратитесь в поддержку: @admgrz"
        )
        edit_message_text_hendler(
            text=error_message,
            chat_id=chat_id,
            message_id=message_id,
            parse_mode="Markdown"
        )
        print(f"Ошибка создания платежа: {e}")

def free_post(callback):
    try:
        bot.answer_callback_query(callback.id)
    except Exception as e:
        print(f"Ошибка ответа на callback: {e}")

    user_id, chat_id, message_id = get_easy_callback(callback)
    # Если есть активный тариф - сразу отправляем на модерацию
    edit_message_text_hendler(chat_id=chat_id, message_id=message_id, text=moderation_text(), reply_markup=main_menu_buttons(), parse_mode="Markdown")
    post = get_save_post(user_id)
    add_post(user_id, post, callback.from_user.username, "Бесплатный пост")



'''
##################################################

                CALLBACK STARTWITH

##################################################
'''
#Прошло модерацию
def approve(callback):
    post_id = int(callback.data.split("_")[1])
    add_approval_status(post_id, "✅ Одобрено")
    content = get_content(post_id)
    price = get_price(post_id)

    

    edit_message_text_hendler(
        chat_id=callback.message.chat.id,
        message_id=callback.message.id,
        text=f"✅ Пост {post_id} одобрен\n--------------------------\n{content}\n--------------------------",
    )
    post_data = get_post_data(post_id)
    if post_data:
        user_id = post_data["user_id"]
        content = post_data["content"]
        content += "\n\n #реклама"

        # Отправляем уведомление автору
        delete_message_one(user_id, get_chat_id(user_id))
        sent_message = bot.send_message(
            user_id, text_after_approve(), reply_markup=main_menu_buttons(), parse_mode="Markdown"
        )
        add_delete_message_id(user_id, sent_message.message_id)

        # Публикуем пост в группе
        for i in range(len(GROUP_CHAT_ID)):
            try:
                sent_message = bot.send_message(GROUP_CHAT_ID[i], content)

                if price == "pay_premium":
                    bot.pin_chat_message(
                        chat_id=GROUP_CHAT_ID[i], 
                        message_id=sent_message.message_id,
                        disable_notification=True
                    )
            except Exception as e:
                print(f"Ошибка отправки в группу: {e}")

#Не прошло модерацию
def reject(callback):
    post_id = int(callback.data.split("_")[1])
    add_approval_status(post_id, "❌ Отклонено")
    user_id = callback.from_user.id
    add_user_status(user_id, f"waiting_reason_{post_id}")
    edit_message_text_hendler(
        chat_id=callback.message.chat.id,
        message_id=callback.message.id,
        text=f"❌ Пост отклонен, напишите причину",
    )

#редактировать пост после оплаты
def rpost(callback):
    try:
        bot.answer_callback_query(callback.id)
    except Exception as e:
        print(f"Ошибка ответа на callback: {e}")

    user_id, chat_id, message_id = get_easy_callback(callback)
    post_id = int(callback.data.split("_")[1])

    add_user_status(user_id, f"waiting_redact_{post_id}")
    edit_message_text_hendler(chat_id=chat_id, message_id=message_id, text=redact_text(), reply_markup=my_posts_buttons(), parse_mode="Markdown")
