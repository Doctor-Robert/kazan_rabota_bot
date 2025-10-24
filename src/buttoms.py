from text import *

load_dotenv()
Configuration.account_id = os.environ.get("YOOKASSA_SHOP_ID")
Configuration.secret_key = os.environ.get("YOOKASSA_SECRET_KEY")


# Главное меню
def main_menu_buttons():
    kb = types.InlineKeyboardMarkup()
    btm1 = types.InlineKeyboardButton(
        text="📤 ВЫЛОЖИТЬ ПОСТ", callback_data="send_post"
    )
    btm2 = types.InlineKeyboardButton(text="📊 МОИ ПОСТЫ", callback_data="profile")
    btm3 = types.InlineKeyboardButton(text="❓ ПОМОЩЬ ", callback_data="help")
    kb.add(btm1)
    kb.add(btm2, btm3)
    return kb

def my_posts_buttons():
    kb = types.InlineKeyboardMarkup()
    btm2 = types.InlineKeyboardButton(text="📊 МОИ ПОСТЫ", callback_data="profile")
    kb.add(btm2)
    return kb


# Возвращение в Главное меню
def back_to_main_menu_button():
    kb = types.InlineKeyboardMarkup()
    btm1 = types.InlineKeyboardButton(
        text="📋 ГЛАВНОЕ МЕНЮ", callback_data="back_to_main_menu"
    )
    kb.add(btm1)
    return kb


def back_to_main_menu_change_button(post_id):
    btm0 = types.InlineKeyboardButton(text="✏️ РЕДАКТИРОВАТЬ", callback_data=f"rpost_{post_id}")
    kb = types.InlineKeyboardMarkup()
    btm1 = types.InlineKeyboardButton(
        text="📋 ГЛАВНОЕ МЕНЮ", callback_data="back_to_main_menu"
    )
    kb.add(btm0)
    kb.add(btm1)
    return kb


def back_to_main_menu_button_reply():
    kb = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    kb.row(types.KeyboardButton("📋 ГЛАВНОЕ МЕНЮ"))  # Правильно
    return kb


def redact_button():
    kb = types.InlineKeyboardMarkup()
    btm1 = types.InlineKeyboardButton(text="✅ ВСЁ ВЕРНО", callback_data="moderation")
    btm2 = types.InlineKeyboardButton(text="✏️ РЕДАКТИРОВАТЬ", callback_data="redact")
    kb.add(btm1, btm2)
    return kb


def pay_button(tarif):
    price = []
    
    if tarif == 'yes':
        price = [75, 149, 499]
    else:
        price = [149, 299, 999]
    
    kb = types.InlineKeyboardMarkup()
    
    if tarif == 'yes':
        btm1 = types.InlineKeyboardButton(f"📦 БАЗОВЫЙ — {price[0]} ₽ 💰", callback_data="pay_basic")
        btm2 = types.InlineKeyboardButton(f"🚀 ПРЕМИУМ — {price[1]} ₽ 💰", callback_data="pay_premium")
        btm3 = types.InlineKeyboardButton(f"💎 БИЗНЕС — {price[2]} ₽/мес 💰", callback_data="pay_hrplus")
    else:
        btm1 = types.InlineKeyboardButton(f"📦 БАЗОВЫЙ — {price[0]} ₽", callback_data="pay_basic")
        btm2 = types.InlineKeyboardButton(f"🚀 ПРЕМИУМ — {price[1]} ₽", callback_data="pay_premium")
        btm3 = types.InlineKeyboardButton(f"💎 БИЗНЕС — {price[2]} ₽/мес", callback_data="pay_hrplus")
    
    btm4 = types.InlineKeyboardButton("📋 ГЛАВНОЕ МЕНЮ", callback_data="back_to_main_menu")
    
    kb.add(btm1)
    kb.add(btm2)
    kb.add(btm3)
    kb.add(btm4)
    return kb


def payment_button(payment_url):
    """Кнопка для перехода к оплате"""
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("💳 Перейти к оплате", url=payment_url))
    # kb.add(
    #     types.InlineKeyboardButton("🔄 Проверить оплату", callback_data="check_payment")
    # )
    kb.add(types.InlineKeyboardButton("⬅️ Назад", callback_data="moderation"))
    return kb


def before_post_button():
    kb = types.InlineKeyboardMarkup()
    btm1 = types.InlineKeyboardButton(
        text="📋 ГЛАВНОЕ МЕНЮ", callback_data="back_to_main_menu"
    )
    btm2 = types.InlineKeyboardButton(text="⬅️ НАЗАД", callback_data="before_post")
    kb.add(btm2)
    kb.add(btm1)
    return kb

def before_post_change_button(post_id):
    kb = types.InlineKeyboardMarkup()
    btm0 = types.InlineKeyboardButton(text="✏️ РЕДАКТИРОВАТЬ", callback_data=f"rpost_{post_id}")
    btm1 = types.InlineKeyboardButton(
        text="📋 ГЛАВНОЕ МЕНЮ", callback_data="back_to_main_menu"
    )
    btm2 = types.InlineKeyboardButton(text="⬅️ НАЗАД", callback_data="before_post")
    kb.add(btm0)
    kb.add(btm2)
    kb.add(btm1)
    return kb


def before_and_next_post_button():
    kb = types.InlineKeyboardMarkup()
    btm1 = types.InlineKeyboardButton(
        text="📋 ГЛАВНОЕ МЕНЮ", callback_data="back_to_main_menu"
    )
    btm2 = types.InlineKeyboardButton(text="⬅️ НАЗАД", callback_data="before_post")
    btm3 = types.InlineKeyboardButton(text="ВПЕРЁД ➡️", callback_data="next_post")
    kb.add(btm2, btm3)
    kb.add(btm1)
    return kb

def before_and_next_post_change_button(post_id):
    kb = types.InlineKeyboardMarkup()
    btm0 = types.InlineKeyboardButton(text="✏️ РЕДАКТИРОВАТЬ", callback_data=f"rpost_{post_id}")
    btm1 = types.InlineKeyboardButton(
        text="📋 ГЛАВНОЕ МЕНЮ", callback_data="back_to_main_menu"
    )
    btm2 = types.InlineKeyboardButton(text="⬅️ НАЗАД", callback_data="before_post")
    btm3 = types.InlineKeyboardButton(text="ВПЕРЁД ➡️", callback_data="next_post")
    kb.add(btm0)
    kb.add(btm2, btm3)
    kb.add(btm1)
    return kb


def next_post_button():
    kb = types.InlineKeyboardMarkup()
    btm1 = types.InlineKeyboardButton(
        text="📋 ГЛАВНОЕ МЕНЮ", callback_data="back_to_main_menu"
    )
    btm2 = types.InlineKeyboardButton(text="ВПЕРЁД ➡️", callback_data="next_post")
    kb.add(btm2)
    kb.add(btm1)
    return kb

def next_post_change_button(post_id):
    kb = types.InlineKeyboardMarkup()
    btm0 = types.InlineKeyboardButton(text="✏️ РЕДАКТИРОВАТЬ", callback_data=f"rpost_{post_id}")
    btm1 = types.InlineKeyboardButton(
        text="📋 ГЛАВНОЕ МЕНЮ", callback_data="back_to_main_menu"
    )
    btm2 = types.InlineKeyboardButton(text="ВПЕРЁД ➡️", callback_data="next_post")
    kb.add(btm0)
    kb.add(btm2)
    kb.add(btm1)
    return kb
