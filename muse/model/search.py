"""Whoosh implementation for Muse to allow blog post searches."""
from whoosh.index import create_in
from whoosh.fields import ID, Schema, STORED, TEXT
from pylons import config, url

from muse.model import Post

schema = Schema(
    title=TEXT(stored=True),
    content=TEXT,
    summary=TEXT(stored=True),
    url=TEXT(stored=True),
    category=STORED
)
index = None

def init_indexes(self):
    """Updates Whoosh indexes with latest posts.  This function should run on
    start-up preferrably.
    """
    index = create_in(config['beaker.cache.data_dir'], schema)
    writer = index.writer()
    for post in Post.all():
        writer.add_document(
            title=post.title,
            content=post.content,
            summary=post.summary,
            url=url(
                controller='blog',
                action='view',
                category=post.category.id,
                id=post.id
            ),
            category={'name': post.category.title, 'slug': post.category.slug},
        )
    writer.commit()