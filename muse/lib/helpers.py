# Copyright (c) 2010 Chris Santiago (http://faltzershq.com/)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""Helper functions"""
import json

from pylons import config, tmpl_context as c, url
from recaptcha.client.captcha import displayhtml
from webhelpers.pylonslib import Flash
from phanpy.helpers import (base, convertdate, converttext, getip,
    htmlencode, htmlfill, slug
)

flash = Flash()

def breadcrumbs():
    """Prepares breadcrumbs for inclusion in page."""
    c.breadcrumbs.append({
        'title': c.title,
        'url': ''
    })
    # Simulate a prepend by reversing the breadcrumb list to add site title and
    # index link, then reverse again.
    c.breadcrumbs.reverse()
    c.breadcrumbs.append({
        'title': c.blog_title,
        'url': c.blog_index
    })
    c.breadcrumbs.reverse()

    return ''

def comment_canedit(user_id):
    """Template helper; returns whether or not the current user is allowed
    to edit the comment.
    """
    if not c.user.id:
        return 'false'

    if c.user.id == user_id or c.user.admin:
        return 'true'

    return 'false'

def comment_editing(comment_id):
    """Template helper; returns whether or not the current comment is being
    edited.
    """
    if c.editing_comment == comment_id:
        return 'true'
    return 'false'

def flash_pop():
    """Grabs from the flash message stack so it can be looped through
    templating.
    """
    c._flash = flash.pop_messages()
    return ''

def recaptcha():
    """Display reCaptcha only if the user is not identified."""
    if c.user.id:
        return ''
    return displayhtml(config.get('recaptcha.public_key', ''))