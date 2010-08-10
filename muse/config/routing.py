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
    map.connect('/new-post', controller='blog', action='new_post')
    map.connect('/new-category', controller='blog', action='new_category')
    map.connect('/account/{action}', controller='account')
    map.connect('/{category}', controller='blog', action='view')
    map.connect('/{category}/{id}', controller='blog', action='view')

    # Remove forward-slashes from URLs.
    redirect_kwargs = dict(_redirect_code='301 Moved Permanently')
    map.redirect('/account/{action}/', '/account/{action}', **redirect_kwargs)
    map.redirect('/{category}/', '/{category}', **redirect_kwargs)
    map.redirect('/{category}/{id}/', '/{category}/{id}', **redirect_kwargs)
    return map
