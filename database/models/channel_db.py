from sqlalchemy import Column, Integer, String,Date,Text,DateTime,BigInteger
from sqlalchemy.sql import exists
from bot.database import base,session
import datetime
from bot import LOGGER
import threading
from bot.database.models.settings_db import get_list_size
LOCK=threading.RLock()

class Channel(base):
    __tablename__ = 'channel'
    id = Column(Integer, primary_key=True)
    chat_id=Column(Integer)
    channel_id=Column(BigInteger)
    subscribers=Column(Integer)
    channel_name=Column(String)
    admin_username = Column(String)
    description=Column(String)
    invite_link=Column(String)

    def __init__(self,chat_id,channel_id,subscribers,channel_name,admin_username,description,invite_link):
        self.chat_id=chat_id
        self.channel_id=channel_id
        self.channel_name=channel_name
        self.subscribers=subscribers
        self.admin_username=admin_username
        self.description=description
        self.invite_link=invite_link

    def __repr__(self):
        return '{}'.format(self.description)
    
    
engine = session.get_bind() 
Channel.__table__.create(bind=engine, checkfirst=True)

class Ban(base):  
    __tablename__ = 'ban_channel'
    id = Column(Integer, primary_key=True)
    channel_id=Column(BigInteger)

    def __init__(self,channel_id):
        self.channel_id=channel_id

    def __repr__(self):
        
        return f'{self.id}'

engine = session.get_bind() 
Ban.__table__.create(bind=engine, checkfirst=True)
    
def channel_data(chat_id,channel_id,channel_name,subscribers,admin_username,description,invite_link):
    with LOCK:
        LOGGER.info(f"New Channel {channel_id} [{channel_name}] by {admin_username}")
        session.add(
                        Channel(chat_id=chat_id,channel_id=int(channel_id),
                            channel_name=channel_name,
                            subscribers=subscribers,
                            admin_username=admin_username,
                            description=description,
                            invite_link=invite_link
                        )
                    )
        session.commit()

def is_channel_exist(channel_id):
    try:
        LOGGER.info(f"Checking Existance of {channel_id}")
        data=session.query(Channel).filter(Channel.channel_id==int(channel_id))
        return session.query(data.exists()).scalar()
    finally:
        session.close()
        
def is_channel_ban(channel_id):
    try:
        LOGGER.info(f"Checking ban status {channel_id}")
        ban=session.query(Ban).filter(Ban.channel_id==str(channel_id))
        return session.query(ban.exists()).scalar()
    finally:
        session.close()
def is_user_not_added_channel(chat_id):
    try:
        data=session.query(Channel).filter(Channel.chat_id==chat_id)
        print(session.query(data.exists()).scalar())
        return session.query(data.exists()).scalar()
    finally:
        session.close()

def delete_channel(channel_id):
    with LOCK:
        LOGGER.info(f'channel removed {channel_id}')
        session.query(Channel).filter(Channel.channel_id==int(channel_id)).delete()
        session.commit()
    
def get_all_channel(chat_id):
    try:
        LOGGER.info(f"Getting Channel registed by {chat_id}")
        return session.query(Channel).filter(Channel.chat_id==chat_id).all()
    finally:
        session.close()
        
def get_channel():
    try:
        return [channel for channel in session.query(Channel).all()]
    finally:
        session.close()
        

    
        
def update_subs(channel_id,subs):
    with LOCK:
        session.query(Channel).filter(Channel.channel_id==channel_id).update({Channel.subscribers:subs})
        session.commit()

def total_channel():
    return session.query(Channel).count()

def total_banned_channel():
    return session.query(Ban).count()

def ban_channel(channel_id):
    with LOCK:
        session.add(Ban(channel_id=int(channel_id)))
        session.commit()
        LOGGER.info(f'channel {channel_id} banned ')
    
def unban_channel(channel_id):
    with LOCK:
        session.query(Ban).filter(Ban.channel_id==int(channel_id)).delete()
        session.commit()

def is_channel_banned(channel_id):
    try:
        ban=session.query(Ban).filter(Ban.channel_id==channel_id)
        return session.query(ban.exists()).scalar()
    finally:
        session.close()
        
def get_channel_by_id(channel_id):
    try :
        return session.query(Channel).filter(Channel.channel_id==int(channel_id)).first()
    finally:
        session.close()
        
def get_banned_channel_list():
    try:
        return [channel.channel_id for channel in session.query(Ban).all()]
    finally:
        session.close()
        
def get_user_channel_count(chat_id):
    try:
        return session.query(Channel).filter(Channel.chat_id==chat_id).count()
    finally:
        session.close()
        
def chunck():
    l=[r.channel_id for r in session.query(Channel).distinct()]
    for i in range(0,len(l),):
        yield l[i:i+get_list_size()]   