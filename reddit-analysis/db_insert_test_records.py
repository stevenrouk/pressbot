from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import SQLITE_DATABASE_URI
from db_create import Base, Comment, Post

# Set up SQLAlchemy engine and bindings
engine = create_engine(SQLITE_DATABASE_URI)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Insert Post
new_post = Post(name='23xlkjo', title='holy crap this is awesome!')
session.add(new_post)
session.commit()

# Insert Comment
new_comment = Comment(name='345lkjsoi', text="i don't think it's that awesome", post=new_post)
session.add(new_comment)
session.commit()
