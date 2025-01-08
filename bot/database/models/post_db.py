from sqlalchemy import Column, Integer, String,Date,Text,DateTime
from bot.database import base,session
import datetime
from bot import LOGGER
import threading

class Post(base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    emoji=Column(String,default=None)
    set_top=Column(String,default=None)
    set_bottom=Column(String,default=None)
    set_caption=Column(String,default=None)

    def __init__(self,emoji,set_top,set_bottom,set_caption):
        self.emoji=emoji
        self.set_top=set_top
        self.set_bottom=set_bottom
        self.set_caption=set_caption

    def __repr__(self):
        return f'{self.id}'
engine = session.get_bind() 
Post.__table__.create(bind=engine, checkfirst=True)

class Button(base):
    __tablename__ = 'button'
    id = Column(Integer, primary_key=True)
    name=Column(String)
    url=Column(String)

    def __init__(self,name,url):
        self.name=name
        self.url=url

    def __repr__(self):
        return f'{self.id}'

engine = session.get_bind() 
Button.__table__.create(bind=engine, checkfirst=True)


LOCK=threading.RLock()


def add_button(name,url):
    with LOCK:
        LOGGER.info(f"Button Added : {name} {url}")
        session.add(Button(name=name,url=url))
        session.commit()    
        
def delete_button():
    try:
        button=session.query(Button).all()
        if button:
            with LOCK:
                    session.query(Button).delete()
                    session.commit()
    finally:
        session.close()
                
def add_emoji(emoji):
    
        post=session.query(Post).filter(Post.id == 1).first()
        with LOCK:
            if not post:
                    session.add(Post(emoji=emoji,set_bottom=None,set_caption=None,set_top=None))
                    session.commit()
            else:
                session.query(Post).filter(Post.id==1).update({Post.emoji:emoji})
                session.commit()
    
    
def add_caption(caption):
    
        post=session.query(Post).filter(Post.id == 1).first()
        with LOCK:
            if not post:
                    session.add(Post(emoji=None,set_bottom=None,set_caption=caption,set_top=None))
                    session.commit()
            else:
                session.query(Post).filter(Post.id==1).update({Post.set_caption:caption})
                session.commit()

        
def add_top_text(text):
    
        post=session.query(Post).filter(Post.id == 1).first()
        with LOCK:
            if not post:
                    session.add(Post(emoji=None,set_bottom=None,set_caption=None,set_top=text))
                    session.commit()
            else:
                session.query(Post).filter(Post.id==1).update({Post.set_top:text})
                session.commit()

        
def add_bottom_text(text):
    
        post=session.query(Post).filter(Post.id == 1).first()
        with LOCK:
            if not post:
                    session.add(Post(emoji=None,set_bottom=text,set_caption=None,set_top=None))
                    session.commit()
            else:
                session.query(Post).filter(Post.id==1).update({Post.set_bottom:text})
                session.commit()
   
        
def get_buttons():
    
        return  session.query(Button).all()
  
        
def get_post():
    
        return  session.query(Post).filter(Post.id==1).first()
   