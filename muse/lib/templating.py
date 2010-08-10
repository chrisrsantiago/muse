import os
import hashlib
try:
    import json
except ImportError:
    import simplejson as json

from pylons import config, request
import suit

def render(template, **kwargs):
    """Provide our own rendering function for suit-python."""
    filepath = os.path.join(config['pylons.paths']['templates'],
        os.path.normpath(template)
    )
    defaultlog = {'hash': {}, 'contents': []}
    try:
        content = open(filepath).read()
    except IOError:
        raise IOError('Template does not exist: %s' % filepath)
    result = suit.execute(config['suit.rules'], content)

    if 'slacks' in request.params and 'slacks' in kwargs:
        # Granted slacks is enabled for this template and receive a request
        # for slacks, then return JSON'd output instead.
        slacks = json.dumps(suit.log, separators=(',',':'))
        suit.log = defaultlog
        response.headerlist = [
            ('Pragma', 'public'),
            ('Expires', '0'),
            ('Cache-Control', 'must-revalidate, post-check=0, pre-check=0'),
            ('Content-type', 'text/json'),
            ('Content-Disposition', 'attachment; filename=slacks.json'),
            ('Content-Length', len(slacks))
        ]
        suit.log = defaultlog
        return slacks
    return result