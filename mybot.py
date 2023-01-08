from reminders_db import RemindersDb, Reminder, validate_rule
from scheduler import ReminderScheduler
from datetime import datetime
from typing import Dict
import telebot
import yaml

with open("config.yaml", 'r') as stream:
    config_loaded = yaml.safe_load(stream)

assert config_loaded is not None

TOKEN = config_loaded['config']['token']

db = RemindersDb()
newReminders: Dict[int, Reminder] = dict()
bot = telebot.TeleBot(TOKEN)

scheduler = ReminderScheduler(db, bot)


@bot.message_handler(content_types=['text'])
def get_text_messages(message: telebot.types.Message) -> None:

    chatId = message.from_user.id

    if message.text.casefold() == "привет":
        response = "Привет, чем я могу тебе помочь?"
        bot.send_message(chatId, response)

    elif message.text == "/help" or message.text == "/start":
        response = """
Доступные команды:
/help - снова показать эту подсказку
/list - показать текущий список напоминаний
/add - добавление нового напоминания
/rem - удаление напоминания
/set_utc_offset - задать часовой пояс
"""
        bot.send_message(chatId, response)

    elif message.text == "/set_utc_offset":
        offsets = db.get_all_offsets()

        response = f"Текущее время сервера {datetime.now().time()}, текущий часовой пояс {offsets.get(chatId, 0)}. Укажи разницу со своим временем в часах числом (например, 2 или -1)"
        bot.send_message(chatId, response)
        bot.register_next_step_handler(message, ask_timezone)

    elif message.text == "/list":
        remindersList = db.list_by_user(chatId)
        reminders = '\n'.join(repr(r) for r in remindersList)
        if not reminders:
            reminders = "- Пусто"

        response = f"""
Твой текущий список напоминаний:
{reminders}
"""
        bot.send_message(chatId, response)

    elif message.text == "/add":
        newReminders[chatId] = Reminder(user_id=chatId)

        response = "О чём тебе напомнить?"
        bot.send_message(chatId, response)
        bot.register_next_step_handler(message, ask_content)

    elif message.text.startswith('/rem'):
        response = "Что ты хочешь удалить? Введи индекс из списка"
        bot.send_message(chatId, response)
        bot.register_next_step_handler(message, ask_rem)

    else:
        response = "Я тебя не понимаю. Напиши /help."
        bot.send_message(chatId, response)


def ask_content(message: telebot.types.Message):
    chatId = message.from_user.id
    newReminders[chatId].content = message.text

    response = "Когда ты хочешь получить напоминание?"
    bot.send_message(chatId, response)
    bot.register_next_step_handler(message, ask_time)


def ask_time(message: telebot.types.Message):

    chatId = message.from_user.id
    rule = message.text

    if not validate_rule(rule):
        response = "Я такое не умею(("
        bot.send_message(chatId, response)
        return

    newReminders[chatId].rule = rule
    db.insert(newReminders[chatId])

    newReminders[chatId] = Reminder()

    response = "Записал"
    bot.send_message(chatId, response)


def ask_rem(message: telebot.types.Message):

    chatId = message.from_user.id
    try:
        idx = int(message.text)
        db.remove(idx)

        response = "Удалил"
        bot.send_message(chatId, response)

    except Exception:
        response = "Не получилось ("
        bot.send_message(chatId, response)


def ask_timezone(message: telebot.types.Message):

    chatId = message.from_user.id
    try:
        tz = int(message.text)
        db.set_user_offset(chatId, tz)

        response = "Установил таймзону"
        bot.send_message(chatId, response)

    except Exception as e:
        response = "Не получилось ("
        bot.send_message(chatId, response)


bot.polling(none_stop=True, interval=1)
