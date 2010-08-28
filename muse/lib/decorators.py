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
        if (
            (member and type == 'guest')
            or (not member and type in ['member', 'admin'])
            or (not admin and type == 'admin')
        ):
            abort(403)

        return func(*args, **kwargs)
    return check