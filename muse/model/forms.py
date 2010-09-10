from pylons import config, tmpl_context as c
from formencode import Schema, FancyValidator
from formencode.validators import (String, StringBoolean, Int, Invalid,
    Email, URL
) 
from sqlalchemy.orm.exc import NoResultFound
from phanpy.validators import OpenId

from muse.model import Category, Post as Post_, User


class CategoryId(Int):
    """Checks against the database to verify that a category exists."""
    def _to_python(self, value, c):
        try:
            category = Category.by_id(value).one()
        except NoResultFound:
            raise Invalid(_('Category does not exist'), value, c)
        return Int._to_python(self, value, c)


class CategoryTitle(String):
    """Checks against the database to verify that a category doesn't exist."""
    def _to_python(self, value, c):
        try:
            category = Category.by_slug(value).one()
            raise Invalid(
                _('There is already a category with that name.'), value, c
            )
        except NoResultFound:
            pass
        return String._to_python(self, value, c)


class PostSlug(String):
    """Checks against the database to verify that a slug is not taken."""
    def _to_python(self, value, c):
        try:
            user = Post_.by_slug(value).one()
            raise Invalid('Slug already in use.', value, c)
        except NoResultFound:
            pass
        return String._to_python(self, value, c)


class Post(Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    title = String(not_empty=True)
    category_id = CategoryId()
    category_title = CategoryTitle()
    slug = PostSlug()
    summary = String()
    content = String(not_empty=True)


class Comment(Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    comment = String(not_empty=True)
    email = Email(not_empty=True, resolve_domain=True)
    name = String(not_empty=True)
    recaptcha_challenge_field = String(not_empty=True)
    recaptcha_response_field = String(not_empty=True)
    url = URL(add_http=True)


class CommentUser(Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    comment = String(not_empty=True)


class Login(Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    openid_identifier = OpenId(not_empty=True)


class Profile(Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    delete = StringBoolean(if_missing=False)
    identifier = OpenId(not_empty=True)
    name = String(not_empty=True)
    email = Email(not_empty=False, resolve_domain=True)
    website = URL(add_http=True)