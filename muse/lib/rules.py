import os
import hashlib

from pylons import config, request, response, tmpl_context as c, url
from pylons.i18n import gettext as _
from rulebox import templating, suitlons

from muse.lib import helpers as h

__all__ = ['gravatar', 'message', 'rules']

def gravatar(params):
    """Return a Gravatar for the given email address."""
    email_hash = hashlib.md5(params['string']).hexdigest()
    rating = params['var']['rating']
    size = params['var']['size']
    format = 'http://www.gravatar.com/avatar/%s?r=%s&s=%s'
    c._gravatar = format % (email_hash, rating, size)
    params['string'] = h.render('_gravatar.tpl')
    return params

def message(params):
    """Displays an information, warning or success message to the user."""
    if params['var']['type'] == 'error':
        c._msg_title = _('Error!')
    elif params['var']['type'] == 'success':
        c._msg_title = _('Success!')
    else:
        c._msg_title = _('For Your Information')
    c._msg_type = params['var']['type']
    c._msg = params['string']
    params['string'] = render('_message.tpl')
    return params

muserules = {
    '[gravatar]':
    {
        'close': '[/gravatar]',
        'functions': [templating.walk, templating.attribute, gravatar],
        'var':
        {
            'equal': templating.default['equal'],
            'log': templating.default['log'],
            'quote': templating.default['quote'],
            'var':
            {
                'rating': 'PG',
                'size': '80',
            }
        }
    },
    '[gravatar':
    {
        'close': ']',
        'create': '[gravatar]',
        'skip': True
    },
    '[message]':
    {
        'close': '[/message]',
        'functions': [templating.walk, templating.attribute, message],
        'var':
        {
            'equal': templating.default['equal'],
            'log': templating.default['log'],
            'quote': templating.default['quote'],
            'var':
            {
                'type': 'info'
            }
        }
    },
    '[message':
    {
        'close': ']',
        'create': '[message]',
        'skip': True
    }
}

# Make sure [call] and [transform] use our helpers.
rules = dict(suitlons.rules.copy(), **muserules)
rules['[call'] = rules['[call'].copy()
rules['[call']['var']['var']['owner'] = h
rules['[transform]'] = rules['[transform]'].copy()
rules['[transform]']['var']['var']['owner'] = h