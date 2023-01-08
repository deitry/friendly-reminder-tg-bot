from reminders_db import RemindersDb
import telebot
import yaml

with open("config.yaml", 'r') as stream:
    config_loaded = yaml.safe_load(stream)

assert config_loaded is not None

TOKEN = config_loaded['config']['token']

bot = telebot.TeleBot(TOKEN)

db = RemindersDb()
db.start()

bot.polling(none_stop=True, interval=1)


@bot.message_handler(content_types=['text'])
def get_text_messages(message: telebot.types.Message) -> None:
    if message.text.casefold() == "привет":
        response = "Привет, чем я могу тебе помочь?"
        bot.send_message(message.from_user.id, response)

    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши привет")

    elif message.text == "/list":
        response = """
Твой текущий список напоминаний:
1. пресс качат
2. Т) бегит
3. Турник
4. Анжуманя
"""
        bot.send_message(message.from_user.id, response)

    elif message.text == "/add":
        response = "Считай что сделано"
        bot.send_message(message.from_user.id, response)
        # bot.register_next_step_handler(message, get_name); #следующий шаг – функция get_name

    elif message.text.startswith('/rem'):
        response = "Что ты хочешь удалить?"
        bot.send_message(message.from_user.id, response)

    else:
        response = "Я тебя не понимаю. Напиши /help."
        bot.send_message(message.from_user.id, response)
