# import datetime
from typing import Any

from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

Base: Any
Base = declarative_base()


class Reminder(Base):
    __tablename__ = 'reminders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    content = Column(String)
    rule = Column(String)

    def __repr__(self) -> str:
        return f"<{self.id=}, {self.user_id=}, {self.content=}, {self.rule=}>"


class RemindersDb:

    def start(self):
        engine = create_engine('sqlite:////home/ubuntu/workspace/bot-reminder/reminders.db')

        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()

        allReminders = session.query(Reminder).all()
        if not allReminders:
            print('time to create new reminders')
            session.add(Reminder(user_id=666, content='бегит', rule="8:30"))
            session.add(Reminder(user_id=666, content='анжуманя', rule="9:30"))
            session.commit()

            allReminders = session.query(Reminder).all()
        else:
            print("already created!")

        for reminder in allReminders:
            print(reminder)
