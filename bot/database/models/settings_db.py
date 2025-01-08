from sqlalchemy import Column, Integer, String, Date, Text, DateTime
from bot.database import base, session
import datetime
from bot import LOGGER
import threading

LOCK = threading.RLock()

class Settings(base):
    __tablename__ = 'settings'
    
    id = Column(Integer, primary_key=True)
    subs_limit = Column(Integer, default=0)
    list_size = Column(Integer, default=25)
    row = Column(Integer, default=5)

    def __repr__(self):
        return f'{self.id}'

engine = session.get_bind() 
Settings.__table__.create(bind=engine, checkfirst=True)




LOCK=threading.RLock()

def add_subs_limit(limit):
    with LOCK:
        settings=session.query(Settings).first()
        if settings:
            session.query(Settings).filter(Settings.id==1).update({Settings.subs_limit:int(limit)})
            session.commit()
        else:
            session.add(Settings(subs_limit=int(limit)))
            session.commit()
            
def add_row(row):
    with LOCK:
        settings=session.query(Settings).first()
        if settings:
            session.query(Settings).filter(Settings.id==1).update({Settings.row:int(row)})
            session.commit()
        else:
            session.add(Settings(row=int(row)))
            session.commit()

def add_list_size(size):
    with LOCK:
        settings=session.query(Settings).first()
        if settings:
            session.query(Settings).filter(Settings.id==1).update({Settings.list_size:int(size)})
            session.commit()
        else:
            session.add(Settings(list_size=int(size)))
            session.commit()

def get_settings():
    try:
        settings = session.query(Settings).first()
        if settings is None:
            return {"subs_limit": "Non défini", "list_size": "Non défini"}
        return settings
    finally:
        session.close()


def get_subcribers_limit():
    settings = session.query(Settings).first()
    if settings is None:
        return "Non défini"
    return settings.subs_limit


def get_list_size():
    settings = session.query(Settings).first()
    if settings is None:
        return "Non défini"
    return settings.list_size

def get_row():
    settings = session.query(Settings).first()
    if settings is None:
        return int(1)
    return settings.row
