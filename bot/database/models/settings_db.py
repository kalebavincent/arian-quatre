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
        return session.query(Settings).first()
    finally:
        session.close() 
        
        
def get_subcribers_limit():
    limit=session.query(Settings).first()
    return limit.subs_limit

def get_list_size():
    limit=session.query(Settings).first()
    return limit.list_size