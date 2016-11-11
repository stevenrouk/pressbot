import datetime
import json
import os
import praw
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys

from config import REDDIT_USER_AGENT, SQLITE_DATABASE_URI
from db_create import Author, Base, Comment, Post

BASEDIR = os.path.dirname(os.path.realpath(__file__))

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

    return session

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
    # set up counts
    post_count = 0
    comment_count = 0
    author_count = 0
    total_comment_count = 0

    # get db session
    session = get_db_session()

    # TODO: create a constant data ingest
    for post in posts:
        comment_count = 0
        # Add post & author
        new_post = get_object(session, Post, reddit_id=post.id)
        if not new_post:
            # Add author first
            new_author = get_object(session, Author, reddit_id=post.author.id)
            if not new_author:
                author = post.author
                new_author = Author(
                    reddit_id=author.id,
                    reddit_fullname=author.fullname,
                    name=author.name,
                    created_date=datetime.datetime.fromtimestamp(author.created),
                )
                session.add(new_author)
                session.commit()
                author_count += 1
                print('wrote author #{}'.format(author_count))

            # Add post
            new_post = Post(
                reddit_id=post.id,
                reddit_fullname=post.fullname,
                author=[new_author],
                created_date=datetime.datetime.fromtimestamp(post.created),
                title=post.title,
                url=post.url,
                num_comments=post.num_comments,
                score=post.score,
                upvotes=post.ups,
                downvotes=post.downs,
            )
            session.add(new_post)
            session.commit()
            post_count += 1
            print('wrote post #{}'.format(post_count))

        # Add comments
        post.replace_more_comments(limit=None, threshold=0)
        for comment in post.comments:
            new_comment = get_object(session, Comment, reddit_id=comment.id)
            if not new_comment:
                # Add author first
                try:
                    new_author = get_object(session, Author, reddit_id=comment.author.id)
                    if not new_author:
                        author = comment.author
                        new_author = Author(
                            reddit_id=author.id,
                            reddit_fullname=author.fullname,
                            name=author.name,
                            created_date=datetime.datetime.fromtimestamp(author.created),
                        )
                        session.add(new_author)
                        session.commit()
                        author_count += 1
                        print('wrote author #{}'.format(author_count))
                except AttributeError as e:
                    print('No author: {}'.format(e), exc_info=True)

                # Add comment
                new_comment = Comment(
                    reddit_id=comment.id,
                    created_date=datetime.datetime.fromtimestamp(comment.created),
                    text=comment.body,
                    author=[new_author],
                    post=new_post,
                )
                session.add(new_comment)
                session.commit()
                comment_count += 1
                total_comment_count += 1
                print('wrote comment #{0} (#{1} overall)'.format(comment_count, total_comment_count))

    print("""
Total Posts: {0}\n\tTotal Comments: {1}\n\t Total Authors: {2}\n
""".format(post_count, total_comment_count, author_count))
    print('\n\n*****************************\n\n')


def mvp_scrape(subreddit='vegan', post_type='hot', limit=10):
    """
    Scrape posts and comments, dump them to text.
    Just to validate some ideas.
    """
    print('Scraping for {}'.format(subreddit))
    file_name = os.path.join(BASEDIR, 'data', 'mvp-{}-subreddit.txt'.format(subreddit))
    post_count = 0
    comment_count = 0
    total_comment_count = 0
    more_comments_count = 0
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

    for post in posts:
        comment_count = 0
        try:
            with open(file_name, 'a') as f:
                f.write(post.title)
                f.write('\n')
                post_count += 1
                print('wrote post #{}'.format(post_count))
            for comment in post.comments:
                if type(comment) == praw.objects.MoreComments:
                    more_comments_count += 1
                else:
                    with open(file_name, 'a') as f:
                        f.write(comment.body)
                        f.write('\n')
                        comment_count += 1
                        total_comment_count += 1
                        print('wrote comment #{0} (#{1} overall)'.format(comment_count, total_comment_count))
        except Exception as e:
            print(e)

    print("""
Done executing for {3}.\n\tTotal Posts: {0}\n\tTotal Comments: {1}\n\t Skipped 'More Comments': {2}\n
""".format(post_count, total_comment_count, more_comments_count, subreddit))
    print('\n\n*****************************\n\n')

def mvp():
    list_of_subreds = [
        'animalrights',
        'animalwelfare',
        'veg',
        'vegetarian',
        'vegetarianism',
        'dietaryvegan',
        'veganrecipes',
        'vegproblems',
    ]
    for subred in list_of_subreds:
        try:
            mvp_scrape(subreddit=subred, limit=100)
        except Exception as e:
            print('Failed for {0}: {1}'.format(subred, e))

if __name__ == '__main__':
    # TODO: Check script args.
    #     - If we tell it to run continuously, do that, but the default is a small test.
    
    if len(sys.argv) == 1:
        posts = get_posts(subreddit='vegan', post_type='hot', limit=1000)
        save_posts(posts)
    elif sys.argv[1] == 'continuous':
        while True:
            for post_type in ('hot', 'new', 'top'):
                posts = get_posts(post_type)
                save_posts(posts)
        posts = get_posts(subreddit='vegan', post_type='hot', limit=10)
        save_posts(posts)
    elif sys.argv[1] == 'mvp':
        mvp_scrape()
    else:
        pass
