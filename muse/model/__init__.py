"""The application's model objects"""
from sqlalchemy import MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = None
metadata = MetaData()
session = scoped_session(sessionmaker(autoflush=True, autocommit=False))
BaseTable = declarative_base(metadata=metadata)

def init_model(sa_engine, create_tables=False):
    """Call me before using any of the tables or classes in the model."""
    session.configure(bind=sa_engine)
    metadata.bind = sa_engine
    engine = sa_engine
    if create_tables:
        BaseTable.metadata.create_all(engine)

from muse.model.entities import Category, Comment, Guest, Post, User
from muse.model import forms