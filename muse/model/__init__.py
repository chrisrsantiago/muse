"""The application's model objects"""
import datetime

from sqlalchemy import and_, Column, ForeignKey, MetaData, types
from sqlalchemy.orm import scoped_session, exc, relation, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from phanpy.helpers import slug as slug

__all__ = [
    'BaseTable', 'Category', 'Comment', 'engine', 'init_model',
    'Guest', 'metadata', 'Post', 'session', 'User'
]

engine = None
metadata = MetaData()
session = scoped_session(sessionmaker(autoflush=True, autocommit=False))
BaseTable = declarative_base(metadata=metadata)

def init_model(sa_engine):
    """Initialize all model objects so that they can be used."""
    session.configure(bind=sa_engine)
    metadata.bind = sa_engine
    engine = sa_engine


class Category(BaseTable):
    __tablename__ = 'categories'

    id = Column(types.Integer(10), primary_key=True)
    title = Column(types.Unicode(255))
    slug = Column(types.Unicode(255), unique=True)
    posts = relation('Post')

    def __init__(self, title, slug=''):
        self.title = title
        self.slug = slug(slug)
        if not self.slug:
            # Automatically generate a slug (URL) from the title if there was
            # none supplied.
            self.slug = slug(self.title)

    def __repr__(self):
        return '<Category: %s - %s>' % (self.title, self.slug)

    @classmethod
    def all(self):
        q = session.query(Category)
        return q.all()

    @classmethod
    def by_id(self, id):
        q = session.query(Category).filter(Category.id == id)
        return q

    @classmethod
    def by_slug(self, category):
        q = session.query(Category).filter(Category.slug == slug(category))
        return q

    @classmethod
    def first(self):
        q = session.query(Category).order_by(Category.id.asc()).limit(1)
        return q.one()


class Comment(BaseTable):
    __tablename__ = 'comments'

    id = Column(types.Integer(10), primary_key=True)
    name = Column(types.Unicode(255), nullable=True)
    email = Column(types.Unicode(255), nullable=True)
    url = Column(types.Unicode(255), nullable=True)
    content = Column(types.UnicodeText)
    post_id = Column(types.Integer(10), ForeignKey('posts.id'))
    post = relation('Post', primaryjoin='Comment.post_id == Post.id')
    user_id = Column(types.Integer(10), ForeignKey('users.id'))
    user = relation('User', primaryjoin='User.id == Comment.user_id')
    ip = Column(types.Unicode(16))
    posted = Column(types.DateTime, default=datetime.datetime.now)
    spam = Column(types.Boolean)

    def __init__(self, post_id, content, ip, **kwargs):
        self.post_id = post_id
        self.content = content
        self.ip = ip
        self.user_id = kwargs.get('user_id', 0)
        self.name = kwargs.get('name', '')
        self.email = kwargs.get('email', '')
        self.url = kwargs.get('url', '')
        self.spam = kwargs.get('spam', 0)

    def __repr__(self):
        try:
            name = self.user.name
        except AttributeError:
            name = self.name
        return '<Comment: #%d - by %s>' % (self.id, name)

    @classmethod
    def by_id(self, id):
        q = session.query(Comment).filter(Comment.id == id)
        return q

    @classmethod
    def by_post(self, id):
        q = session.query(Comment).filter(Comment.post_id == id)
        return q

    @classmethod
    def by_user(self, id):
        q = session.query(User).filter(User.id == id)
        return q


class Guest(object):
    id = 0
    admin = 0
    name = u'Anonymous'


class Post(BaseTable):
    __tablename__ = 'posts'

    id = Column(types.Integer(10), primary_key=True)
    title = Column(types.Unicode(255))
    content = Column(types.UnicodeText)
    summary = Column(types.UnicodeText, nullable=True)
    slug = Column(types.Unicode(255), unique=True)
    category_id = Column(types.Integer(10), ForeignKey('categories.id'))
    category = relation('Category')
    user_id = Column(types.Integer(10), ForeignKey('users.id'))
    user = relation('User')
    posted = Column(types.DateTime, default=datetime.datetime.now)
    comments = relation('Comment', order_by=['id'])
    comments_count = Column(types.Integer(10), nullable=True, default=0)

    def __init__(self, title, category_id, content, user_id, **kwargs):
        self.title = title
        self.category_id = category_id
        self.content = content
        self.user_id = user_id
        self.slug = slug(kwargs.get('slug', ''))
        if not self.slug:
            # Automatically generate a slug (URL) from the title if there was
            # none supplied.
            self.slug = slug(self.title)
        self.summary = kwargs.get('summary', '')

    def __repr__(self):
        return '<Post: "%s" by %s>' % (self.title, self.user.name)

    @classmethod
    def all(self):
        q = session.query(Post).order_by(Post.posted.desc())
        return q.all()

    @classmethod
    def by_category(self, id):
        q = session.query(Post).filter(Post.category_id == id)
        return q

    @classmethod
    def by_id(self, id):
        q = session.query(Post).filter(Post.id == id)
        return q

    @classmethod
    def by_slug(self, slug):
        q = session.query(Post).filter(Post.slug == slug)
        return q

    @classmethod
    def by_slug_category(self, slug, category):
        q = session.query(Post).filter(
            and_(Post.slug == slug, Category.slug == category)
        )
        return q

    @classmethod
    def by_user(self, id):
        q = session.query(Post).filter(Post.user_id == id)
        return q


class User(BaseTable):
    __tablename__ = 'users'

    id = Column(types.Integer(10), primary_key=True)
    name = Column(types.Unicode(255))
    identifier = Column(types.Unicode(255), unique=True)
    email = Column(types.Unicode(255))
    website = Column(types.Unicode(255))
    admin = Column(types.Boolean)
    ip = Column(types.Unicode(16))
    comments = relation('Comment', order_by=Comment.id.desc())
    posts = relation('Post')

    def __init__(self, name, identifier, ip, **kwargs):
        self.name = name
        self.identifier = identifier
        self.ip = ip
        self.email = kwargs.get('email', '')
        self.website = kwargs.get('website', '')
        self.admin = kwargs.get('admin', 0)

    def __repr__(self):
        return '<User: %s - %s>' % (self.name, self.identifier)

    @classmethod
    def all(self):
        q = session.query(User).order_by(User.id.asc())
        return q.all()

    @classmethod
    def by_id(self, id):
        q = session.query(User).filter(User.id == id)
        return q

    @classmethod
    def by_identifier(self, identifier):
        q = session.query(User).filter(User.identifier == identifier)
        return q

    @classmethod
    def by_name(self, name):
        q = session.query(User).filter(User.name == name)
        return q

    @classmethod
    def first(self):
        q = session.query(User).order_by(User.id.asc()).limit(1)
        return q.one()