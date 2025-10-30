from yookassa import Configuration, Payment
from dotenv import load_dotenv
from datetime import datetime
from telebot import types
import threading
import telebot
import sqlite3
import uuid
import time
import os

# ТАРИФЫ
TARIFFS = {
    "pay_basic": {
        "amount": 149.00,
        "description": "📊 БАЗОВЫЙ — 149 ₽",
        "label": "ОДИН ПОСТ",
    },
    "pay_premium": {
        "amount": 299.00,
        "description": "⚡ ПРЕМИУМ — 299 ₽",
        "label": "ПОСТ С ЗАКРЕПОМ",
    },
    "pay_hrplus": {
        "amount": 999.00,
        "description": "💼 БИЗНЕС — 999 ₽/мес",
        "label": "ПОДПИСКА НА МЕСЯЦ",
    },
}

TARIFFS_DISCOUNT_50 = {
    "pay_basic": {
        "amount": 75.00,
        "description": "📊 БАЗОВЫЙ — 75 ₽",
        "label": "ОДИН ПОСТ",
    },
    "pay_premium": {
        "amount": 149.00,
        "description": "⚡ ПРЕМИУМ — 149 ₽",
        "label": "ПОСТ С ЗАКРЕПОМ",
    },
    "pay_hrplus": {
        "amount": 499.00,
        "description": "💼 БИЗНЕС — 499 ₽/мес",
        "label": "ПОДПИСКА НА МЕСЯЦ",
    },
}

# CALLBACK
CALLBACK = [
    "help",
    "back_to_main_menu",
    "send_post",
    "redact",
    "moderation",
    "pay_basic",
    "pay_premium",
    "pay_hrplus",
    "profile",
    "before_post",
    "next_post",
    "free_post",
]

#Команды

COMMANDS = ["start", "chat_id", "admin", "send", "show_users", "add_pay_basic", "add_pay_hrplus", "send_info_all_users", "discount_yes", "discount_no", "send_show_post"]

# CHATS ID
GROUP_CHAT_ID = [-1001374673969, -1001746396097]
