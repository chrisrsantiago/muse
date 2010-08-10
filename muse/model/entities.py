import datetime
import re

from elixir import *
from sqlalchemy import and_

__all__ = ['Category', 'Comment', 'Guest', 'Post', 'User']

def generate_slug(title):
    """Automatically generates a slug (URL) if there was none supplied.
    The title attribute is lowercased, and all irregular characters
    are substituted with a dash instead.
    """
    return re.sub('([^A-Za-z0-9_-])', '-', title).lower()

class Category(Entity):
    using_options(tablename='categories')
    has_many('posts', of_kind='Post')

    id = Field(Integer(10), primary_key=True)
    title = Field(Unicode(255))
    description = Field(UnicodeText, nullable=True)
    slug = Field(Unicode(255), unique=True, default=generate_slug)

    def __init__(self, title, description='', slug=''):
        self.title = title
        self.description = description
        self.slug = slug

    def __repr__(self):
        return '<Category: %s - %s>' % (self.title, self.slug)

    @classmethod
    def get_by_id(self, category):
        category = Category.query.filter(Category.slug == category).one()
        return category

class Comment(Entity):
    using_options(tablename='comments')
    belongs_to('post', of_kind='Post')
    belongs_to('user', of_kind='User')

    id = Field(Integer(10), primary_key=True)
    name = Field(Unicode(200), nullable=True)
    email = Field(Unicode(255), nullable=True)
    url = Field(Unicode(255), nullable=True)
    content = Field(UnicodeText)
    ip = Field(Unicode(16))
    posted = Field(Date, default=datetime.datetime.now)
    approved = Field(Integer(1))

    def __init__(self, post_id, content, name='', email='', url='', ip='',
        user_id=0, approved=1, **kwargs
    ):
        self.post_id = post_id
        self.name = name
        self.email = email
        self.content = content
        self.url = url
        self.ip = ip
        self.user_id = user_id
        self.approved = approved

    def __repr__(self):
        return '<Comment: #%d - by %s>' % (self.id, self.name)


class Guest(object):
    id = 0
    name = 'Anonymous'
    admin = 0


class Post(Entity):
    using_options(tablename='posts')
    has_many('comments', of_kind='Comment', order_by=['id', 'posted'])
    belongs_to('author', of_kind='User')
    belongs_to('category', of_kind='Category')

    id = Field(Integer(10), primary_key=True)
    title = Field(Unicode(255))
    contents = Field(UnicodeText)
    posted = Field(Date, default=datetime.datetime.now)
    slug = Field(Unicode(255), default=generate_slug)
    summary = Field(UnicodeText)

    def __init__(self, title, category, contents, author_id, posted='',
        slug='', summary=''
    ):
        self.title = title
        self.category_id = category_id
        self.contents = contents
        self.author_id = author_id
        self.posted = posted
        self.slug = slug
        self.summary = summary

    def __repr__(self):
        return '<Post: "%s" by %s>' % (self.title, self.author.name)

    @classmethod
    def get_all(self):
        posts = Post.query.order_by(Post.posted.desc()).all()
        return posts

    @classmethod
    def get_by_slug(self, slug, category):
        post = Post.query.filter(
            and_(Post.slug == slug, Category.slug == category)
        ).one()
        post.comments_count = len(post.comments)
        return post

class User(Entity):
    using_options(tablename='users')
    has_many('comments', of_kind='Comment')
    has_many('posts', of_kind='Post')

    id = Field(Integer(10), primary_key=True)
    name = Field(Unicode(255))
    email = Field(Unicode(255))
    identifier = Field(Unicode(255))
    admin = Field(Boolean)

    def __init__(self, name, email, identifier, admin=0):
        self.name = name
        self.email = email
        self.identifier = identifier
        self.admin = admin

    def __repr__(self):
        return '<User: %s - %s>' % (self.name, self.identifier)

    @classmethod
    def get_by_identifier(self, identifier):
        user = User.query.filter(User.identifier == identifier).one()
        return user

    @classmethod
    def get_by_id(self, id):
        user = User.query.filter(User.id == id).one()
        return user