from sqlalchemy import Column, Integer, String, Date, Text, DateTime, BigInteger
from bot.database import base, session
import datetime
from bot import LOGGER
import threading

LOCK = threading.RLock()

class Promo(base):
    __tablename__ = 'promo'
    
    id = Column(Integer, primary_key=True)
    channel = Column(BigInteger)
    message_id = Column(Integer)
    
    def __init__(self, channel, message_id):
        self.channel = channel
        self.message_id = message_id

    def __repr__(self):
        return f'{self.id}'

engine = session.get_bind() 
Promo.__table__.create(bind=engine, checkfirst=True)

    
class PaidPromo(base):
    __tablename__ = 'paid_promo'
    id = Column(Integer, primary_key=True)
    channel=Column(BigInteger)
    message_id=Column(Integer)
    
    def __init__(self,channel,message_id):
        self.channel=channel
        self.message_id=message_id
        
    def __repr__(self):
        return f'{self.id}'

LOCK=threading.RLock()

engine = session.get_bind() 
PaidPromo.__table__.create(bind=engine, checkfirst=True)

def add_paidpromo(channel_id,message_id):
    with LOCK:
        session.add(PaidPromo(channel=int(channel_id),message_id=message_id))
        session.commit()
        
def get_paidpromo():
    try:
        return session.query(PaidPromo).all()
    finally:
        session.close()
        
def delete_paid_promo():
    with LOCK:
        session.query(PaidPromo).delete()
        session.commit()
        
        
def save_message_ids(channel_id,message_id):
    promo=session.query(Promo).filter(Promo.channel ==channel_id).all()
    if not len(promo):
        session.add(Promo(channel=channel_id,message_id=message_id))
        session.commit()
    if len(promo):
        session.query(Promo).filter(Promo.channel ==channel_id).update({Promo.message_id:message_id})
        session.commit()
        
        
def get_promo():
    try:
        return session.query(Promo).all()
    finally:
        session.close()
        
def delete_promo():
    with LOCK:
        session.query(Promo).delete()
        session.commit()
        