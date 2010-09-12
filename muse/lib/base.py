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

"""The base Controller API

Provides the BaseController class for subclassing.
"""
from pylons import config, request, session, tmpl_context as c
from pylons.controllers import WSGIController
from pylons.decorators import cache
from pylons.i18n import get_lang, set_lang
from pylons.i18n.translation import ugettext as _
from sqlalchemy.orm.exc import NoResultFound
from phanpy.templating import render

from muse import model
from muse.lib import helpers as h

__all__ = ['_', 'BaseController', 'h', 'render']

class BaseController(WSGIController):
    def __before__(self):
        @cache.beaker_cache(**config['cache_options'])
        def get_categories():
            return model.Category.all()

        @cache.beaker_cache(**config['cache_options'])
        def get_user():
            try:
                return model.User.by_id(session['userid']).one()
            except (KeyError, NoResultFound):
                try:
                    del session['userid']
                    session.save()
                except KeyError:
                    pass
                return model.Guest()
        try:
            set_lang(request.GET['language'])
        except KeyError:
            pass
        c.breadcrumbs = []
        c.categories = get_categories()
        c.user = get_user()

    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']
        try:
            return WSGIController.__call__(self, environ, start_response)
        finally:
            model.session.remove()