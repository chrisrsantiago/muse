"""Setup the scribo application"""
import os
import logging

import pylons.test

from muse.config.environment import load_environment
from muse import model

log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Muse setup script.

    Do not run directly.  Instead, run:

        paster setup-app config.ini
    """

    # Don't reload the app if it was loaded under the testing environment
    if not pylons.test.pylonsapp:
        load_environment(conf.global_conf, conf.local_conf)
    # Whoosh has a habit of complaining when there is no data directory,
    # even though this is created by Beaker soon.
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filepath_data = os.path.join(root, 'data')
    try:
        os.mkdir(filepath_data)
    except (WindowsError, OSError), e:
        print e
    # Create all of the database tables and whatnot.
    model.metadata.create_all(bind=model.engine)
    # Create the default category
    category = model.Category(u'Uncategorized')
    model.session.add(category)
    model.session.commit()
    # It's done.
    print """

    SUCCESS
    ==========
    Your blog is ready for use.  The next step is to point your browser
    to wherever muse is accessible from and register your administrator
    account.

    If you have not setup muse to be accessible from the web, then your
    best bet is to try deploying muse by starting up the paster server, and
    accessing through the given port name:

        paster serve --daemon config.ini

    If you use Apache or lighttpd, then you can deploy muse by using FastCGI,
    or by proxying to it via mod_proxy.  More information on deployment and
    relevant options are available on the Pylons Book website:

    http://pylonsbook.com/en/1.1/deployment.html#deployment-options

    Thank you for using muse.  If you experience any issues or have any
    feedback, then submit a ticket, and I'll address it ASAP:

    http://github.com/faltzer/muse
    """

if __name__ == '__main__':
    print 'This script is not supposed to be run directly.'
    print 'To setup muse, run: paster setup-app config.ini'