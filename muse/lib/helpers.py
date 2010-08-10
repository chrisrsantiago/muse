"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
import re
import htmlentitydefs


from pylons import cache, config, tmpl_context as c
from pylons.i18n.translation import ugettext as _
from recaptcha.client.captcha import displayhtml
import formencode
import suit
from webhelpers.html import escape, HTML, literal, url_escape
from webhelpers.html.converters import markdown, textile, nl2br
from lxml.html.clean import Cleaner

from muse.lib.templating import render

_char = re.compile(r'&(\w+?);')
_dec  = re.compile(r'&#(\d{2,4});')
_hex  = re.compile(r'&#x(\d{2,4});')

def _get_htmlentitydefs(m):
    try:
        return htmlentitydefs.entitydefs[m.group(1)]
    except KeyError:
        return m.group(0)

def base(string, base='base.tpl'):
    """Wrap the current content against a base template."""
    try:
        c.user = c.user.to_json()
    except AttributeError:
        # Assume that it is an instance of Guest() and let it slide.
        pass
    c.config = config
    c.categories = make_categories(c.categories)
    c.content = string
    return render(base)

def convert_text(string, parser=''):
    """Takes formatted input to return mark-up based on the given parsers,
    markdown or textile.  If neither are chosen, sanitized HTML is instead 
    returned.
    """
    if not parser:
        parser = config['post_parser']
    string = unescape(string)
    if parser == 'markdown':
        return markdown(string, safe_mode='escape')
    if parser == 'textile':
        return textile(string, sanitize=True, encoding='utf-8')    
    # Since no parser was selected, return sanitized HTML output instead.
    cleaner = Cleaner(add_nofollow=True, comments=True, frames=True,
        forms=True, javascript=True, links=True, meta=True,
        page_structure=True, processing_instructions=True,
        safe_attrs_only=True, style=True, scripts=True
    )
    return cleaner.clean_html(literal(string))

def format_date(posted, format=''):
    """Convert a datetime.datetime into string representation using the date
    settings specified in the configuration INI file or by the format argument.
    """
    if not format:
        format = config['blog_dateformat']
    try:
        return posted.strftime(format)
    except AttributeError, TypeError:
        return _('Unknown')

def get_ip():
    """Retrieve a client's IP address."""
    return unicode(request.environ.get('HTTP_X_FORWARDED_FOR',
        request.environ.get('REMOTE_ADDR', '127.0.0.1')
    ))

def htmlfill(error, form):
    return formencode.htmlfill.render(form=form, defaults=request.params,
        errors=(error and error.unpack_errors()),
        encoding=response.determine_charset()
    )

def unescape(string):
    """Back-replace html-safe sequences to special characters."""
    result = _hex.sub(lambda x: unichr(int(x.group(1), 16)),
        _dec.sub(lambda x: unichr(int(x.group(1))),
        _char.sub(_get_htmlentitydefs, string))
    )
    if string.__class__ != unicode:
        return result.encode('utf-8')
    else:
        return result

def make_posts(iterable):
    """Template helper; iterate through the list of posts and convert the
    instances to dictionaries so PySUIT can loop through the values.
    """
    posts = []
    for i, post in enumerate(iterable):
        post = post.to_dict(deep={'category': {}, 'comments': {}})
        post['comments_count'] = len(post['comments'])
        post['rowcolor'] = (i % 2 and '1' or '0')
        post['posted'] = format_date(post['posted'])
        del post['comments']
        posts.append(post)
    return posts

def make_categories(iterable):
    """Template helper; iterate through the list of comments and convert the
    instances to dictionaries so PySUIT can loop through the values.
    """
    categories = []
    for i, category in enumerate(iterable):
        category = category.to_dict(deep={'posts': {}})
        category['posts_count'] = len(category['posts'])
        category['rowcolor'] = (i % 2 and '1' or '0')
        del category['posts']
        categories.append(category)
    return categories

def make_comments(iterable):
    """Template helper; iterate through the list of comments and convert the
    instances to dictionaries so PySUIT can loop through the values.
    """
    comments = []
    for i, comment in enumerate(iterable):
        comment = comment.to_dict(deep={'user': {}})
        comment['rowcolor'] = (i % 2 and '1' or '0')
        comment['posted'] = format_date(comment['posted'])
        comments.append(comment)
    return comments

def post():
    """Template helper; format dates for articles and set-up recaptcha."""
    try:
        c.apost.posted = c.post.posted.strftime(config['blog_dateformat'])
        c.comments = make_comments(c.post.comments)
    except AttributeError:
        pass
    c.recaptcha = displayhtml(config['recaptcha_public_key'])
    return ''
