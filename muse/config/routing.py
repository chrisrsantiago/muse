"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from pylons import config
from routes import Mapper

def make_map(config):
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'])
    map.minimization = False

    map.connect('/error/{action}', controller='error')
    map.connect('/error/{action}/{id}', controller='error')

    map.connect('/', controller='blog', action='index')
    map.connect('/rss', controller='blog', action='index', rss='true')
    map.connect('/new-post', controller='blog', action='new_post')
    map.connect('/login', controller='account', action='login')
    map.connect('/login_complete', controller='account', action='login_complete')
    map.connect('/logout', controller='account', action='logout')
    map.connect('/profile', controller='account', action='profile')
    map.connect('/profile/{id:\d+}', controller='account', action='profile')
    map.connect('/profile/{id:\d+}/edit', controller='account', action='profile',
        edit='true'
    )
    map.connect('/{category}', controller='blog', action='view')
    map.connect('/{category}/{slug}', controller='blog', action='view')
    map.connect('/{category}/{slug}/edit', controller='blog', action='view',
        edit='true'
    )
    map.connect(
        '/{category}/{slug}/edit-comment/{edit_comment:\d+}',
        controller='blog',
        action='view'
    )
    return map
