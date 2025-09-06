import telebot
import os
from dotenv import load_dotenv

# .env faylni yuklaymiz
load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN)

# Webhook ni o'chiramiz
bot.delete_webhook()
print("✅ Webhook o‘chirildi!")
