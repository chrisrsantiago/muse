"""Whoosh implementation for Muse to allow post searches."""
import json

from whoosh.index import create_in
from whoosh.fields import ID, Schema, STORED, TEXT
from pylons import config

from muse.model import Post

__all__ = ['build_indexes', 'index', 'schema']

schema = Schema(
    title=TEXT(stored=True),
    content=TEXT,
    summary=TEXT(stored=True),
    url=TEXT(stored=True),
    category=STORED
)

def build_indexes():
    """Updates Whoosh indexes with latest posts.  This function should run
    on start-up preferrably.
    """
    index = create_in(config['pylons.cache_dir'], schema)
    writer = index.writer()
    for post in Post.all():
        writer.add_document(
            title=post.title,
            content=post.content,
            summary=post.summary,
            url=u'%s' % (json.dumps({
                'controller': 'blog',
                'action': 'view',
                'category': post.category.slug,
                'slug': post.slug
            })),
            category=u'%s' % (json.dumps(
                {'name': post.category.title, 'slug': post.category.slug}
            )),
        )
    writer.commit()
    return index