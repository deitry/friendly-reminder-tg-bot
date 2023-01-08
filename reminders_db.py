# import datetime
from typing import Any, List, Dict

from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from dateutil import parser
from datetime import datetime


Base: Any
Base = declarative_base()


def rule_to_datetime(rule: str) -> datetime:
    return datetime.combine(datetime.today(), parser.parse(rule).time())


def validate_rule(rule: str) -> bool:
    try:
        return rule_to_datetime(rule).time() is not None

    except Exception:
        return False


class Reminder(Base):
    __tablename__ = 'reminders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    content = Column(String)
    rule = Column(String)

    def __repr__(self) -> str:
        return f"{self.id}. {self.content}, {self.rule}"


class UserSettings(Base):
    __tablename__ = 'user_settings'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    timezone = Column(Integer)


class RemindersDb:

    def __init__(self):
        self.engine = create_engine(
            'sqlite:////home/ubuntu/workspace/bot-reminder/reminders.db')

        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        # allReminders = self.session.query(Reminder).all()
        # if not allReminders:
        #     print('time to create new reminders')
        #     self.session.add(
        #         Reminder(user_id=666, content='бегит', rule="8:30"))
        #     self.session.add(
        #         Reminder(user_id=666, content='анжуманя', rule="9:30"))
        #     self.session.commit()

        #     allReminders = self.session.query(Reminder).all()
        # else:
        #     print("already created!")

        # for reminder in allReminders:
        #     print(reminder)

    def insert(self, reminder: Reminder):
        session = sessionmaker(bind=self.engine)()

        session.add(reminder)
        session.commit()

    def remove(self, index: int):
        session = sessionmaker(bind=self.engine)()

        reminder = session.query(Reminder).filter(Reminder.id == index).first()
        session.delete(reminder)
        session.commit()

    def list_by_user(self, userId: int) -> list[Reminder]:
        session = sessionmaker(bind=self.engine)()

        allReminders = session.query(Reminder).filter(
            Reminder.user_id == userId)
        return allReminders.all()

    def list_all(self) -> list[Reminder]:
        session = sessionmaker(bind=self.engine)()

        allReminders = session.query(Reminder)
        return allReminders.all()

    def set_user_offset(self, user_id: int, time_offset: int):
        session = sessionmaker(bind=self.engine)()

        settings = session.query(UserSettings).filter(UserSettings.user_id == user_id).first()
        if settings is None:
            settings = UserSettings(user_id=user_id)
            session.add(settings)
            session.commit()

        settings.timezone = int(time_offset)

        session.commit()

    def get_all_offsets(self) -> Dict[int, int]:
        session = sessionmaker(bind=self.engine)()

        allReminders: List[UserSettings] = session.query(UserSettings).all()

        return {p.user_id: p.timezone for p in allReminders}
