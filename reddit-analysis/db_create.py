from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship
from sqlalchemy import create_engine

from config import SQLITE_DATABASE_URI

Base = declarative_base()

class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True)
    reddit_id = Column(String(250), nullable=False)
    reddit_fullname = Column(String(250))
    created_date = Column(DateTime)
    title = Column(String(250))
    url = Column(String(250))
    num_comments = Column(Integer)
    score = Column(Integer)
    upvotes = Column(Integer)
    downvotes = Column(Integer)
    comments = relationship('Comment', backref='post')
    author = relationship('Author', backref='post')

class Comment(Base):
    __tablename__ = 'comment'

    id = Column(Integer, primary_key=True)
    reddit_id = Column(String(250), nullable=False)
    reddit_fullname = Column(String(250))
    created_date = Column(DateTime)
    text = Column(String(250))
    post_id = Column(Integer, ForeignKey('post.id'))
    author = relationship('Author', backref='comment')

class Author(Base):
    __tablename__ = 'author'

    id = Column(Integer, primary_key=True)
    reddit_id = Column(String(250), nullable=False)
    reddit_fullname = Column(String(250))
    name = Column(String(250))
    created_date = Column(DateTime)
    post_id = Column(Integer, ForeignKey('post.id'))
    comment_id = Column(Integer, ForeignKey('comment.id'))

# Create database
engine = create_engine(SQLITE_DATABASE_URI)
Base.metadata.create_all(engine)
