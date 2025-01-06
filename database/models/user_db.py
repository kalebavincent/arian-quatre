

from sqlalchemy import Column, Integer, String,Date,Text,DateTime
from bot.database import base,session
import datetime
from bot import LOGGER
import threading

LOCK=threading.RLock()

class User(base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    chat_id=Column(Integer)
    first_name= Column(String)
    last_name=Column(String)
    username = Column(String)
    date = Column(Date,default=datetime.date.today())

    def __init__(self, chat_id, first_name, last_name,username):
        self.chat_id = chat_id
        self.first_name=first_name
        self.last_name=last_name
        self.username=username

    def __repr__(self):
        return "<id {}>".format(self.id)
    
User.__table__.create(bind=session.get_bind(), checkfirst=True)


class Admin(base):
    __tablename__='admins'
    id=Column(Integer,primary_key=True)
    chat_id=Column(Integer)

    def __init__(self,chat_id):
        self.chat_id=chat_id  

    def __repr__(self):
        return f'{self.id}'
    
engine = session.get_bind() 
Admin.__table__.create(bind=engine, checkfirst=True)

def add_user(message):
    
    user=session.query(User).filter(User.chat_id == message.chat.id).all()
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username
    chat_id = message.chat.id
    
    if first_name == None:
        first_name = 'None'
    if last_name == None:
        last_name = 'None'
    if username == None:
        username = 'None'
    if chat_id == None:
        chat_id = 'None'
    with LOCK:
        if not len(user):
            session.add(User(chat_id=message.chat.id,username=username,first_name=first_name,last_name=last_name))
            session.commit()
            LOGGER.info('New User : chat_id {} username {}'.format(chat_id,username))
        if len(user):
            session.query(User).filter(User.chat_id == message.from_user.id).update({User.first_name:first_name,User.last_name:last_name,User.username:username},synchronize_session='fetch')
            session.commit()
        
def delete_user(chat_id):
    with LOCK:
        session.query(User).filter(User.chat_id==chat_id).delete()
        session.commit()   

def get_admin():
    try:
        return [admin.chat_id for admin in session.query(Admin).all()]
    finally :
        session.close()
def get_all():
    try:
        return [user.chat_id for user in session.query(User).all()]
    finally :
        session.close()
        
def add_admin(chat_id):
    with LOCK:
        session.add(Admin(chat_id=int(chat_id)))
        session.commit()

def total_users():
    return session.query(User).count()

def total_admin():
    return session.query(Admin).count()

def get_all_user_data():
    return session.query(User).all()

def get_user_username(chat_id):
    user=session.query(User).filter(User.chat_id==chat_id).first()
    return user.username