from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

from config import SQLITE_DATABASE_URI

Base = declarative_base()

class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True)
    reddit_id = Column(String(250), nullable=False)
    author_name = Column(String(250))
    author_id = Column(String(250))
    published_date = Column(DateTime)
    title = Column(String(250))
    url = Column(String(250))
    text = Column(String(250))
    num_comments = Column(Integer)
    score = Column(Integer)
    upvotes = Column(Integer)
    downvotes = Column(Integer)

class Comment(Base):
    __tablename__ = 'comment'

    id = Column(Integer, primary_key=True)
    reddit_id = Column(String(250), nullable=False)
    author_name = Column(String(250))
    author_id = Column(String(250))
    published_date = Column(DateTime)
    text = Column(String(250))
    post_id = Column(Integer, ForeignKey('post.id'))
    post = relationship(Post)

# Create database
engine = create_engine(SQLITE_DATABASE_URI)
Base.metadata.create_all(engine)
