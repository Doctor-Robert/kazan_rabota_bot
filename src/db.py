from lists import *

load_dotenv()
TELEBOT_KEY = os.environ.get("TELEBOT_KEY")
ADMIN_ID = os.environ.get("ADMIN_ID")
bot = telebot.TeleBot(TELEBOT_KEY)


def init_db():
    conn = sqlite3.connect("work_bot.db")
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            user_status TEXT DEFAULT "",
            delete_message_id INT,
            chat_id INT,
            discount DEFAULT "no",
            users_meaning_1 TEXT,
            users_meaning_2 TEXT,
            save_post TEXT
        )
    """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS posts (
            post_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            content TEXT,
            status TEXT DEFAULT 'pending',
            approval_status TEXT DEFAULT '🕐 На модерации',
            admin_comment TEXT DEFAULT NULL,
            price TEXT,
            posts_meaning_1 TEXT,
            posts_meaning_2 TEXT,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS payments (
            payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            yookassa_payment_id TEXT UNIQUE,
            tariff_type TEXT,
            amount REAL,
            status TEXT DEFAULT 'pending',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            payments_meaning_1 TEXT,
            payments_meaning_2 TEXT,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS user_tariffs (
            user_id INTEGER PRIMARY KEY,
            tariff_type TEXT,
            purchased_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            expires_at DATETIME,
            posts_available INTEGER DEFAULT 0,
            user_tariffs_meaning_1 TEXT,
            user_tariffs_meaning_2 TEXT,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
    """
    )
    conn.commit()
    conn.close()


def get_db_connection():
    conn = sqlite3.connect("work_bot.db")
    conn.row_factory = sqlite3.Row
    return conn


################## ФУНКЦИИ ДОБАВЛЕНИЯ И ИЗВЛЕЧЕНИЯ ИЗ БД #####################


#Добавить пост и отправить админам
def add_post(user_id, content, username, price, status="🕐 На модерации"):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO posts (user_id, content, approval_status, price) VALUES (?, ?, ?, ?)",
        (user_id, content, status, price),
    )
    post_id = cur.lastrowid
    conn.commit()
    conn.close()

    send_post_to_admins(post_id, content, username, price)
    return post_id

def send_post_to_admins(post_id, content, username, price):
    kb = types.InlineKeyboardMarkup()
    btm1 = types.InlineKeyboardButton(
        text="✅ Одобрить", callback_data=f"approve_{post_id}"
    )
    btm2 = types.InlineKeyboardButton(
        text="❌ Отклонить", callback_data=f"reject_{post_id}"
    )
    kb.add(btm1, btm2)

    try:
        text = f"👤 Новая заявка на публикацию #post_{post_id}\n\nАвтор: [@{username}]\nТариф: {price}\n\nСодержание:\n————————————\n{content}\n————————————"
        bot.send_message(ADMIN_ID, text, reply_markup=kb)
    except:
        text = f"ПОВТОРНАЯ ОТПРАВКА ИЗ-ЗА ОШИБКИ!👤 Новая заявка на публикацию #post_{post_id}\n\nАвтор: [@{username}]\nТариф: {price}\n\nСодержание:\n————————————\n{content}\n————————————"
        bot.send_message(ADMIN_ID, text, reply_markup=kb)

#Получить все из таблиц posts / users
def get_all_posts(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM posts WHERE user_id = ? ORDER BY post_id DESC", (user_id,)
    )
    posts = cur.fetchall()
    conn.close()
    return posts

def get_all_users():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        'SELECT * FROM users',
    )
    result = cur.fetchall()
    conn.close()

    return result

#user_id / content
def get_post_data(post_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT user_id, content FROM posts WHERE post_id = ?", (post_id,))
    result = cur.fetchone()
    conn.close()
    return dict(result) if result else None



#discount
def get_discount(user_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT discount FROM users WHERE user_id = ?", (user_id,))
    result = cur.fetchone()
    conn.close()
    if result:
        return result["discount"]
    return "no"

def add_discount(user_id, discount):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "UPDATE users SET discount = ? WHERE user_id = ?", (discount, user_id)
    )
    conn.commit()
    conn.close()

#content
def add_content(post_id, content):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "UPDATE posts SET content = ? WHERE post_id = ?", (content, post_id)
    )
    conn.commit()
    conn.close()

def get_content(post_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT content FROM posts WHERE post_id = ?", (post_id,))
    result = cur.fetchone()
    conn.close()
    if result:
        return result["content"]
    return ""

#user / nickname / chat_id
def add_user_and_nickname(user_id, username, chat_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT OR IGNORE INTO users (user_id, username, chat_id) VALUES (?, ?, ?)",
        (user_id, username, chat_id),
    )
    conn.commit()
    conn.close()

def get_chat_id(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT chat_id FROM users WHERE user_id = ?", (user_id,))
    result = cur.fetchone()
    conn.close()
    if result and result["chat_id"]:
        return int(result["chat_id"])
    return None

#delete_message
def add_delete_message_id(user_id, delete_message_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE users SET delete_message_id = ? WHERE user_id = ?",
        (delete_message_id, user_id),
    )
    conn.commit()
    conn.close()

def get_delete_message_id(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT delete_message_id FROM users WHERE user_id = ?", (user_id,))
    result = cur.fetchone()
    conn.close()
    if result and result["delete_message_id"]:
        return int(result["delete_message_id"])
    return None

#user_status
def add_user_status(user_id, user_status):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "UPDATE users SET user_status = ? WHERE user_id = ?", (user_status, user_id)
    )
    conn.commit()
    conn.close()

def get_user_status(user_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT user_status FROM users WHERE user_id = ?", (user_id,))
    result = cur.fetchone()
    conn.close()
    if result:
        return result["user_status"]
    return ""

#save_post
def add_save_post(user_id, save_post):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "UPDATE users SET save_post = ? WHERE user_id = ?", (save_post, user_id)
    )
    conn.commit()
    conn.close()

def get_save_post(user_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT save_post FROM users WHERE user_id = ?", (user_id,))
    result = cur.fetchone()
    conn.close()
    if result:
        return result["save_post"]
    return ""

#posts_available
def add_posts_available(user_id, posts_available):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE user_tariffs SET posts_available = ? WHERE user_id = ?",
        (posts_available, user_id),
    )
    conn.commit()
    conn.close()

def get_posts_available(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT posts_available FROM user_tariffs WHERE user_id = ?", (user_id,)
    )
    result = cur.fetchone()
    conn.close()
    if result:
        return int(result["posts_available"])
    return 0  # Возвращаем 0 вместо None



#approval_status
def add_approval_status(post_id, approval_status):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "UPDATE posts SET approval_status = ? WHERE post_id = ?",
        (approval_status, post_id)
    )
    conn.commit()
    conn.close()

#expires_at
def get_expires_at(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT expires_at FROM user_tariffs WHERE user_id = ?", (user_id,))
    result = cur.fetchone()
    conn.close()
    if result and result["expires_at"]:
        return result["expires_at"]
    return None

#price
def get_price(post_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT price FROM posts WHERE post_id = ?", (post_id,))
    result = cur.fetchone()
    conn.close()
    if result:
        return result["price"]
    return ""



#ФУНКЦИИ ОПЛАТЫ
def create_payment(user_id, yookassa_payment_id, tariff_type, amount):
    """Создание записи о платеже"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO payments (user_id, yookassa_payment_id, tariff_type, amount) VALUES (?, ?, ?, ?)",
        (user_id, yookassa_payment_id, tariff_type, amount),
    )
    conn.commit()
    conn.close()

def update_payment_status(yookassa_payment_id, status):
    """Обновление статуса платежа"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE payments SET status = ? WHERE yookassa_payment_id = ?",
        (status, yookassa_payment_id),
    )
    conn.commit()
    conn.close()

def get_payment_by_id(yookassa_payment_id):
    """Получение информации о платеже"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM payments WHERE yookassa_payment_id = ?", (yookassa_payment_id,)
    )
    result = cur.fetchone()
    conn.close()
    return result

def activate_tariff(user_id, tariff_type):
    """Активация тарифа после оплаты"""
    conn = get_db_connection()
    cur = conn.cursor()

    # Определяем количество постов и срок действия
    tariff_config = {
        "pay_basic": {"posts": 1, "days": 0},
        "pay_premium": {"posts": 1, "days": 0},
        "pay_hrplus": {"posts": 0, "days": 30},
    }

    from datetime import datetime, timedelta

    config = tariff_config.get(tariff_type, {"posts": 1, "days": 7})
    expires_at = datetime.now() + timedelta(days=config["days"])

    cur.execute(
        """
        INSERT OR REPLACE INTO user_tariffs 
        (user_id, tariff_type, expires_at, posts_available) 
        VALUES (?, ?, ?, ?)
    """,
        (user_id, tariff_type, expires_at, config["posts"]),
    )

    conn.commit()
    conn.close()



