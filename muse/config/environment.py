"""Pylons environment configuration"""
import os

import pylons
from pylons.configuration import PylonsConfig
from sqlalchemy import engine_from_config, orm

from muse.config.routing import make_map
import muse.lib.app_globals as app_globals
import muse.model as model
import muse.lib.helpers
import muse.lib.rules as rules

def load_environment(global_conf, app_conf):
    """Configure the Pylons environment via the ``pylons.config``
    object
    """
    config = PylonsConfig()

    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    paths = dict(root=root,
                 controllers=os.path.join(root, 'controllers'),
                 static_files=os.path.join(root, 'public'),
                 templates=os.path.join(root, 'templates'))

    # Initialize config with the basic options
    config.init_app(global_conf, app_conf, package='muse', paths=paths)
    config['routes.map'] = make_map(config)
    config['pylons.app_globals'] = app_globals.Globals(config)
    config['pylons.h'] = muse.lib.helpers

    # Setup cache object as early as possible
    pylons.cache._push_object(config['pylons.app_globals'].cache)
    # Setup cache options dict to pass to @cache.beaker_cache.
    config['cache_options'] = {
        'query_args': True,
        'expire': config.get('cache_expire', 3600),
        'invalidate_on_startup': True
    }
    # Setup SQLAlchemy
    config['pylons.app_globals'].sa_engine = engine_from_config(config,
        'sqlalchemy.'
    )
    model.init_model(config['pylons.app_globals'].sa_engine)
    # Setup SUIT rules.
    config['suit.rules'] = rules.rules

    return config