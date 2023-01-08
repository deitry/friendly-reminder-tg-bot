from reminders_db import RemindersDb, validate_rule, rule_to_datetime
import schedule
import datetime
import telebot
import time
from threading import Thread


class ReminderScheduler(Thread):

    def __init__(self, db: RemindersDb, bot: telebot.TeleBot):
        Thread.__init__(self)
        self.daemon = True

        self.db = db
        self.bot = bot
        self.last = datetime.datetime.now()

        schedule.every().minute.at(":00").do(job, this=self)
        # schedule.every(1).seconds.do(job, this=self)
        self.start()

    def run(self):
        while True:
            schedule.run_pending()
            time.sleep(1)


def job(this: ReminderScheduler):
    now = datetime.datetime.now()
    offsets = this.db.get_all_offsets()

    if now > this.last:
        reminders = this.db.list_all()
        for r in reminders:
            if validate_rule(r.rule):
                offset = datetime.timedelta(hours=offsets.get(r.user_id, 0))
                t = rule_to_datetime(r.rule) - offset

                if t > this.last and t <= now:
                    this.bot.send_message(r.user_id, r.content)

    this.last = now
