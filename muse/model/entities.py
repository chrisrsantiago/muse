import datetime

from elixir import *
from sqlalchemy import and_

from muse.lib import helpers as h

__all__ = ['Category', 'Comment', 'Guest', 'Post', 'User']

class Category(Entity):
    using_options(tablename='categories')
    has_many('posts', of_kind='Post')

    id = Field(Integer(10), primary_key=True)
    title = Field(Unicode(255))
    slug = Field(Unicode(255), unique=True)

    def __init__(self, title, slug=''):
        self.title = title
        self.slug = h.generate_slug(slug)
        if not self.slug:
            # Automatically generate a slug (URL) from the title if there was
            # none supplied.
            self.slug = h.generate_slug(self.title)

    def __repr__(self):
        return '<Category: %s - %s>' % (self.title, self.slug)

    @classmethod
    def get_all(self):
        categories = Category.query.all()
        return categories

    @classmethod
    def get_by_id(self, id):
        category = Category.query.filter(Category.id == id).one()
        return category

    @classmethod
    def get_by_slug(self, category):
        category = Category.query.filter(
            Category.slug == h.generate_slug(category)
        ).one()
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

    def __init__(self, post_id, content, ip, **kwargs):
        self.post_id = post_id
        self.content = content
        self.ip = ip
        self.user_id = kwargs.get('user_id', '')
        self.name = kwargs.get('name', '')
        self.email = kwargs.get('email', '')
        self.url = kwargs.get('url', '')

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
    content = Field(UnicodeText)
    posted = Field(Date, default=datetime.datetime.now)
    slug = Field(Unicode(255), unique=True)
    summary = Field(UnicodeText, nullable=True)
    comments_count = Field(Integer(10), nullable=True, default=0)

    def __init__(self, title, category_id, content, author_id, **kwargs):
        self.title = title
        self.category_id = category_id
        self.content = content
        self.author_id = author_id
        self.slug = h.generate_slug(kwargs.get('slug', ''))
        if not self.slug:
            # Automatically generate a slug (URL) from the title if there was
            # none supplied.
            self.slug = h.generate_slug(self.title)
        self.summary = kwargs.get('summary', '')

    def __repr__(self):
        return '<Post: "%s" by %s>' % (self.title, self.author.name)

    @classmethod
    def get_all(self):
        posts = Post.query.order_by(Post.posted.desc()).all()
        return posts

    @classmethod
    def get_by_slug(self, slug):
        post = Post.query.filter(
            and_(Post.slug == h.generate_slug(slug))
        ).one()
        post.comments_count = len(post.comments)
        return post

    @classmethod
    def get_by_slug_category(self, slug, category):
        post = Post.query.filter(
            and_(Post.slug == h.generate_slug(slug), Category.slug == category)
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
    identifier = Field(Unicode(255), unique=True)
    admin = Field(Boolean)

    def __init__(self, name, identifier, email='', admin=0):
        self.name = name
        self.email = email
        self.identifier = identifier
        self.admin = admin

    def __repr__(self):
        return '<User: %s - %s>' % (self.name, self.identifier)

    @classmethod
    def get_by_name(self, identifier):
        user = User.query.filter(User.name == value).one()
        return user

    @classmethod
    def get_by_identifier(self, identifier):
        user = User.query.filter(User.identifier == identifier).one()
        return user

    @classmethod
    def get_by_id(self, id):
        user = User.query.filter(User.id == id).one()
        return user