import json
import os
import praw
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import REDDIT_USER_AGENT, SQLITE_DATABASE_URI
from db_create import Base, Comment, Post

##########################
##########################
######    Test structure for continuous scraper
##########################
##########################

def get_object(session, model, **kwargs):
    """
    Helper function to check if object already exists in database.
    """
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        return None

def get_db_session():
    """
    Set up SQLAlchemy engine and bindings.
    """
    engine = create_engine(SQLITE_DATABASE_URI)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

def get_posts(subreddit='vegan', post_type='hot', limit=1000):
    # Set up Reddit objects
    user_agent = REDDIT_USER_AGENT
    r = praw.Reddit(user_agent=user_agent)
    subreddit_object = r.get_subreddit(subreddit)

    # Get posts from the vegan subreddit
    if post_type == 'hot':
        posts = subreddit_object.get_hot(limit=limit)
    elif post_type == 'top':
        posts = subreddit_object.get_top(limit=limit)
    elif post_type == 'new':
        posts = subreddit_object.get_new(limit=limit)
    else:
        posts = None

    return posts

def save_posts(posts):
    session = get_db_session()

    # TODO: check for uniqueness. Only insert things we haven't seen before.
    # TODO: create a constant data ingest
    for post in posts:
        # Add post
        new_post = get_object(session, Post, reddit_id=)    # TODO: fill in unique reddit object id
        if not new_post:
            new_post = Post(
                reddit_id=,    # TODO: fill in unique reddit object id
                author_name=,    # TODO: fill in author name
                author_id=,    # TODO: fill in author id
                published_date=,    # TODO: fill in published date
                title=post.title,
                url=post.url,
                text=post.text,
                num_comments=post.num_comments,
                score=post.score,
                upvotes=post.ups,
                downvotes=post.downs,
            )
            session.add(new_post)
            session.commit()

        # Add comments
        for comment in post.comments:
            new_comment = get_object(session, Comment, reddit_id=)    # TODO: fill in unique reddit object id
            if not new_comment:
                new_comment = Comment(
                    reddit_id=,    # TODO: fill in
                    author_name=,    # TODO: fill in
                    author_id=,    # TODO: fill in
                    published_date=,    # TODO: fill in
                    text=,    # TODO: fill in
                    post=new_post,

                )
                session.add(new_comment)
                session.commit()




if __name__ == '__main__':
    # TODO: Check script args.
    #     - If we tell it to run continuously, do that, but the default is a small test.
    test = True
    if test:
        posts = get_posts(subreddit='vegan', post_type='hot', limit=10)
        save_posts(posts)
    else:
        while True:
            for post_type in ('hot', 'new', 'top'):
                posts = get_posts(post_type)
                save_posts(posts)
    
