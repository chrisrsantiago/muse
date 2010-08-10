"""The base Controller API

Provides the BaseController class for subclassing.
"""
import os
import hashlib

from pylons import session, request, tmpl_context as c
from pylons.i18n import get_lang, set_lang
from pylons.i18n.translation import ugettext as _
from pylons.controllers import WSGIController
from pylons.decorators import cache
import elixir
from sqlalchemy.orm.exc import NoResultFound
import suit

from muse.lib.templating import render
from muse import model
__all__ = ['_', 'BaseController', 'render']

class BaseController(WSGIController):
    def __before__(self):
        @cache.beaker_cache(expire=3600 * 24, invalidate_on_startup=True)
        def get_categories():
            return model.Category.query.all()

        @cache.beaker_cache(expire=3600 * 24, invalidate_on_startup=True)
        def get_user():
            try:
                return model.User.get_by_id(session['userid'])
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
        c.categories = get_categories()
        c.user = get_user()
        suit.log = {'hash': {}, 'contents': []}

    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']
        try:
            return WSGIController.__call__(self, environ, start_response)
        finally:
            elixir.session.remove()