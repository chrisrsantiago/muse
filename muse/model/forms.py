from formencode import Schema
from formencode.validators import String, Int, Email, OpenId, URL, Invalid
from sqlalchemy.orm.exc import NoResultFound
from pylons import config, tmpl_context as c

from muse.model import User

class Username(String):
    def _to_python(self, value, c):
        try:
            user = User.query.filter(User.name == value).one()
            raise Invalid('Username Taken', value, c)
        except NoResultFound:
            pass
        return String._to_python(self, value, c)


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