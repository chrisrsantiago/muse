"""Whoosh implementation for Muse to allow post searches."""
import json

from whoosh.index import create_in
from whoosh.fields import ID, Schema, STORED, TEXT
from webhelpers.html.render import sanitize
from pylons import config

from muse.model import Post

__all__ = ['build_indexes', 'index', 'schema']

schema = Schema(
    title=TEXT(stored=True),
    content=TEXT(stored=True),
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
            title=sanitize(post.title),
            # strip HTML tags so search results aren't comprised of partial
            # HTML tags thus ruining the page.
            content=sanitize(post.content),
            summary=u'%s' % (sanitize(post.summary),),
            url=json.dumps(
                {
                    'controller': 'blog',
                    'action': 'view',
                    'category': post.category.slug,
                    'slug': post.slug
                },
                ensure_ascii=False
            ),
            category=json.dumps(
                {
                'name': sanitize(post.category.title),
                'slug': post.category.slug
                },
                ensure_ascii=False
            )
        )
    writer.commit()
    return index