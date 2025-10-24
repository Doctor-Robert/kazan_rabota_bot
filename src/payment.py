from get_easy_func import *

# Настройка ЮKassa
Configuration.account_id = os.environ.get("YOOKASSA_SHOP_ID")
Configuration.secret_key = os.environ.get("YOOKASSA_SECRET_KEY")

def create_payment_link(user_id, tariff_type, amount, description):
    """Создание платежа в ЮKassa с email для чека"""
    idempotence_key = str(uuid.uuid4())
    
    payment = Payment.create({
        "amount": {
            "value": f"{amount:.2f}",
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://t.me/Gruzchik_Kazan_bot"
        },
        "capture": True,
        "description": description,
        "metadata": {
            "user_id": user_id,
            "tariff_type": tariff_type
        },
        "receipt": {
            "customer": {
                "email": f"user{user_id}@yookassa.ru"  # Временный email
            },
            "items": [
                {
                    "description": description[:128],
                    "quantity": "1",
                    "amount": {
                        "value": f"{amount:.2f}",
                        "currency": "RUB"
                    },
                    "vat_code": "1",
                    "payment_mode": "full_payment",
                    "payment_subject": "service"
                }
            ]
        }
    }, idempotence_key)
    
    return payment

def start_payment_checking(payment_id, chat_id, message_id, user_id, tariff_type, username):
    """Запуск проверки статуса платежа"""
    thread = threading.Thread(
        target=check_payment_status, 
        args=(payment_id, chat_id, message_id, user_id, tariff_type, username)
    )
    thread.daemon = True
    thread.start()

def check_payment_status(payment_id, chat_id, message_id, user_id, tariff_type, username):
    """Проверка статуса платежа"""
    for i in range(30):  # 5 минут проверки
        time.sleep(10)
        
        try:
            payment_info = Payment.find_one(payment_id)
            
            if payment_info.status == "succeeded":
                # Обновляем статус и активируем тариф
                update_payment_status(payment_id, "succeeded")
                activate_tariff(user_id, tariff_type)


                # УВЕДОМЛЕНИЕ О УСПЕШНОЙ ОПЛАТЕ
                success_message = (
                    "✅ *ОПЛАТА УСПЕШНО ПРОЙДЕНА!* \n\n"
                    
                    "🔄 *Что дальше?*\n"
                    "▫️ Мы проверим ваш пост\n"  
                    "▫️ Вы получите уведомление\n"
                    "▫️ Пост появится в ленте\n\n"
                    
                    "🙏 *Спасибо за доверие!*\n"
                    "Ваше объявление увидят тысячи соискателей! 👥"
                )

                posts_available = get_posts_available(user_id)
                add_posts_available(user_id, posts_available - 1)

                post = get_save_post(user_id)
                add_post(user_id, post, username, tariff_type)

                try:
                    edit_message_text_hendler(
                        text=success_message,
                        chat_id=chat_id, 
                        message_id=message_id,
                        reply_markup=main_menu_buttons(),
                        parse_mode="Markdown"
                    )
                except Exception as e:
                    print(f"сообщение уже изменено: {e}")

                    if "message is not modified" not in str(e):
                        bot.send_message(
                            chat_id=chat_id, 
                            text=success_message, 
                            reply_markup=main_menu_buttons(),
                            parse_mode="Markdown"
                        )

                break
                
            elif payment_info.status == "canceled":
                update_payment_status(payment_id, "canceled")
                edit_message_text_hendler(
                    text="❌ *Оплата не прошла*\n\nВы можете попробовать снова",
                    chat_id=chat_id, 
                    message_id=message_id,
                    parse_mode="Markdown"
                )
                break
                
        except Exception as e:
            print(f"Ошибка проверки платежа: {e}")
    
    # Если время вышло
    payment = get_payment_by_id(payment_id)
    if payment and payment['status'] == 'pending':
        update_payment_status(payment_id, "timeout")