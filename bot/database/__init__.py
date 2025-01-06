# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from bot import DATABASE_URI

base = declarative_base()

def initdb() -> scoped_session:
    engine = create_engine(DATABASE_URI)
    base.metadata.bind = engine
    base.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))

session = initdb()
