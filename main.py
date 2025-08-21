import os
from dotenv import load_dotenv
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# .env faylni yuklash
load_dotenv()

# TOKENni olish
TOKEN = os.getenv("TOKEN")

user_modes = {}

bot = telebot.TeleBot(TOKEN)
waiting_users = []
chat_pairs = {}
online_users = set()

# Start komandasi
@bot.message_handler(commands=["start"])
def start(message):
    markup = InlineKeyboardMarkup(row_width=1)
    dub = InlineKeyboardButton("➕Начать диалог➕", callback_data="bir")
    btn_continue = InlineKeyboardButton("Поддерживать❤️", callback_data="danat")
    markup.add(dub, btn_continue)

    bot.send_message(
        message.chat.id,
        "Привет, " + message.from_user.first_name + "! 👋\nДобро пожаловать в анонимный чат-бот! 🎭",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "bir")
def check_subscription(call):
    markup = InlineKeyboardMarkup(row_width=1)
    dub = InlineKeyboardButton("Назад", callback_data="nazat")

    markup.add(dub)

    bot.edit_message_text(
        """/find Поиск собеседника
 /stop Закончить диалог
 /next Следующий 
 /online Живые люди""",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup
    )
    
@bot.callback_query_handler(func=lambda call: call.data == "nazat")
def check_subscription(call):
    markup = InlineKeyboardMarkup(row_width=1)
    dub = InlineKeyboardButton("➕Начать диалог➕", callback_data="bir")
    btn_continue = InlineKeyboardButton("Поддерживать❤️", callback_data="danat")

    markup.add(dub, btn_continue)

    bot.edit_message_text(
        "Пожалуйста, выберите меню.",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup
    )
    
@bot.message_handler(commands=['find'])
def find(message):
    user = message.from_user.id

    if user in chat_pairs:
        bot.reply_to(message, "❗️ Вы уже участвуете в разговоре.")
        return

    if user in waiting_users:
        bot.reply_to(message, "⏳ Вы уже ждете интервьюера...")
        return

    if waiting_users:
        partner = waiting_users.pop(0)  
        if partner == user: 
            waiting_users.append(user)
            bot.reply_to(message, "⏳ Интервьюер ждет...")
            return

        chat_pairs[user] = partner
        chat_pairs[partner] = user

        bot.send_message(user, "🔗 Собеседник найден! Вы можете отправить сообщение.")
        bot.send_message(partner, "🔗 Собеседник найден! Вы можете отправить сообщение.")
    else:
        waiting_users.append(user)
        bot.reply_to(message, "⏳ Интервьюер ждет...")

# STOP
@bot.message_handler(commands=['stop'])
def stop(message):
    user = message.from_user.id

    if user in chat_pairs:
        partner = chat_pairs[user]
        del chat_pairs[user]
        if partner in chat_pairs:
            del chat_pairs[partner]
            bot.send_message(partner, "❌ Собеседник завершил разговор.")
        bot.reply_to(message, "❌ Вы покинули беседу.")
    elif user in waiting_users:
        waiting_users.remove(user)
        bot.reply_to(message, "❌ Поиск отменен.")
    else:
        bot.reply_to(message, "❗️ Вас нет в чате.")

# NEXT
@bot.message_handler(commands=['next'])
def next_user(message):
    stop(message) 
    find(message)  

# ONLINE
@bot.message_handler(commands=['online'])
def online(message):
    pairs_count = len(chat_pairs) // 2
    waiting_count = len(waiting_users)
    bot.reply_to(
        message,
        f"👥 Онлайн: {len(online_users)}\n"
        f"💬 Ожидающий: {waiting_count}\n"
        f"🔗 Активные разговоры: {pairs_count}"
    )

@bot.message_handler(content_types=['text', 'photo', 'video', 'document', 'audio', 'voice', 'sticker'])
def relay_message(message):
    user = message.from_user.id
    if user not in chat_pairs:
        bot.reply_to(message, "❗️ Вы не участвуете в разговоре. Используйте команду /начинать")
        return

    partner = chat_pairs[user]
    try:
        bot.copy_message(chat_id=partner, from_chat_id=message.chat.id, message_id=message.message_id)
    except Exception as e:
        bot.reply_to(message, "❌ Произошла ошибка при отправке сообщения.")
        
@bot.callback_query_handler(func=lambda call: call.data == "danat")
def check_subscription(call):
    markup = InlineKeyboardMarkup(row_width=1)
    dub = InlineKeyboardButton("❤️Дoнат💖", url="https://tirikchilik.uz/anilan")
    dub1 = InlineKeyboardButton("Назад", callback_data="nazat")

    markup.add(dub, dub1)

    bot.edit_message_text(
        "Поддержите наших админов💖",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup
    )

bot.polling()
