"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers.  The functions in this module are available to
templates via the [call /] or [transform] rules.

For example, if I wanted to fetch a user's IP, I would only have to call:

    [call function="get_ip" / ]

If I wanted to format some text for Markdown syntax, one would go:
    
    [transform function="convert_text" parser="markdown"]*Roar*[/transform]
"""
import re

from pylons import cache, config, request, response, tmpl_context as c
from pylons.i18n.translation import ugettext as _
from recaptcha.client.captcha import displayhtml
from dateutil import parser as dateutil
from formencode import htmlfill as htmlfill_
from webhelpers.pylonslib import Flash
from webhelpers.html import escape, HTML, literal, url_escape
from webhelpers.html.converters import textile, nl2br
from markupsafe import Markup
from lxml.html.clean import Cleaner
import suit

from muse.lib.markdown import markdown
from muse.lib.templating import render


flash = Flash()

def base(string, base='base.tpl'):
    """Wrap the current content against a base template."""
    c.content = string
    return render(base)

def convert_text(string, parser=''):
    """Takes formatted input to return mark-up based on the given parsers,
    markdown or textile.  If neither are chosen, sanitized HTML is instead 
    returned.
    """
    if not parser:
        parser = config['post.parser']
    string = Markup(string).unescape()
    if parser == 'markdown':
        return markdown.convert(string)
    if parser == 'textile':
        return textile(string, sanitize=True, encoding='utf-8')    
    # Since no parser was selected, return sanitized HTML output instead.
    cleaner = Cleaner(add_nofollow=True, comments=True, frames=True,
        forms=True, javascript=True, links=True, meta=True,
        page_structure=True, processing_instructions=True,
        safe_attrs_only=True, style=True, scripts=True
    )
    return cleaner.clean_html(literal(string))

def convert_datetime(date, format=''):
    """Convert a datetime.datetime into string representation using the date
    settings specified in the configuration INI file or by the format argument.
    """
    if not format:
        format = config['blog.dateformat']
    try:
        return date.strftime(format)
    except AttributeError:
        return dateutil.parse(date).strftime(format)
    except TypeError:
        return _('Unknown')

def get_ip():
    """Retrieve a client's IP address."""
    return request.environ.get(
        'HTTP_X_FORWARDED_FOR',
        request.environ.get('REMOTE_ADDR', '127.0.0.1')
    )


def generate_slug(string):
    """The title converted to all lowercase, and all irregular characters
    are substituted with a dash instead."""
    regex = re.compile(r"\W+", re.U)
    string = re.sub(
        r'^\W+|\W+$',
        '',
        re.sub(regex, '-', string.replace('_', '-'))
    )
    return string.lower()

def htmlfill(error, form):
    return htmlfill_.render(form=form, defaults=request.params,
        errors=(error and error.unpack_errors()),
        encoding=response.determine_charset()
    )

def recaptcha():
    if c.user.id:
        return ''
    return displayhtml(config.get('recaptcha.public_key', ''))