import telebot
import os

token = os.environ['TELEGRAM_TOKEN']

bot = telebot.TeleBot(token)

@bot.message_handler(commands = ['start'])
def handle_start(m):
    bot.send_message(m.chat.id, "Hola")

bot.polling()