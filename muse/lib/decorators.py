from decorator import decorator
from pylons import tmpl_context as c
from pylons.controllers.util import abort

from muse.lib.base import render

def require(type):
    """Restricts a controller's action to a user whom has not logged in."""
    @decorator
    def check(func, *args, **kwargs):
        member = (c.user.id != 0)
        admin = (c.user.admin == 1)
        """
            if member and i want a GUEST = Guest Check
            if not a member and i want a member = Member Check
            if not admin and i want admin = Admin Check
        """
        if ((member and type == 'guest')
            or (not member and type in ['member', 'admin'])
            or (not admin and type == 'admin')
        ):
            abort(403)

        return func(*args, **kwargs)
    return check