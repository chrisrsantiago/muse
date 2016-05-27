import logging
import json

from pylons import config, request, response, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons.decorators import cache, secure
from routes import request_config
from sqlalchemy.orm.exc import NoResultFound
from akismet import Akismet
from formencode import Schema, validators
from formencode.schema import SimpleFormValidator
from whoosh.highlight import highlight, HtmlFormatter, ContextFragmenter
from whoosh.qparser import MultifieldParser
from webhelpers.feedgenerator import Atom1Feed

from muse.lib import search
from muse.lib.base import _, BaseController, h, render
from muse import model

log = logging.getLogger(__name__)
index = search.build_indexes()

__all__ = [
    'BlogController', 'CategoryId', 'CategoryTitle', 'CategoryForm',
    'CommentForm', 'CommentUserForm', 'index', 'PostForm' 
]

class CategoryId(validators.Int):
    """Checks against the database to verify that a category exists."""
    def _to_python(self, value, c):
        try:
            category = model.Category.by_id(value).one()
        except NoResultFound:
            raise validators.Invalid(_('Category does not exist'), value, c)
        return validators.Int._to_python(self, value, c)


class CategoryTitle(validators.UnicodeString):
    """Checks against the database to verify that a category doesn't exist."""
    def _to_python(self, value, c):
        try:
            category = model.Category.by_slug(value).one()
            raise validators.Invalid(
                _('There is already a category with that name.'), value, c
            )
        except NoResultFound:
            pass
        return validators.UnicodeString._to_python(self, value, c)


class CategoryForm(Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    delete = validators.StringBoolean(if_missing=False)
    title = CategoryTitle(not_empty=True, strip=True)


class CommentForm(Schema):
    allow_extra_fields = True
    filter_extra_fields = False
    comment = validators.UnicodeString(not_empty=True, strip=True)
    email = validators.Email(not_empty=True, resolve_domain=True)
    name = validators.UnicodeString(not_empty=True, strip=True)
    url = validators.URL(add_http=True)


class CommentUserForm(Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    comment = validators.UnicodeString(not_empty=True, strip=True)
    delete = validators.StringBoolean(if_missing=False)


class PostForm(Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    delete = validators.StringBoolean(if_missing=False)
    title = validators.UnicodeString(not_empty=True, strip=True)
    category_id = CategoryId()
    category_title = CategoryTitle()
    slug = validators.UnicodeString(strip=True)
    summary = validators.UnicodeString()
    content = validators.UnicodeString(not_empty=True, strip=True)


class BlogController(BaseController):
    def index(self, rss=False):
        """The default page is loaded, as no post has been specified."""
        @cache.beaker_cache(**config['cache_options'])
        def load_posts():
            try:
                return model.Post.all()
            except NoResultFound:
                return
        c.posts = load_posts()

        if rss:
            return self.rss(c.posts)

        return render('index.tpl', slacks=True)

    @secure.authenticate_form
    def edit_category(self, category_view):
        try:
            form = CategoryForm().to_python(request.POST)
            if form['delete']:
                posts = model.Post.by_category(c.category.id)
                for post in posts.all():
                    model.Comment.by_post(post.id).delete()
                posts.delete()
                model.Category.by_id(c.category.id).delete()
                model.session.commit()
                h.flash(_('Category deleted successfully.'), 'success')
                redirect_url = url(controller='blog', action='index')
            else:
                c.category.title = form['title']
                model.session.commit()
                h.flash(_('Category edited successfully.'), 'success')
                redirect_url = url(
                    controller='blog',
                    action='view',
                    category=c.category.slug
                )
            redirect(redirect_url)
        except validators.Invalid, e:
            return h.htmlfill(e, form=category_view)

    @secure.authenticate_form
    def edit_comment(self, comment, post):
        try:
            form = CommentUserForm().to_python(request.POST)
            if form['delete']:
                model.Comment.by_id(comment.id).delete()
                c.post.comments_count -= 1
                model.session.commit()
                h.flash(_('Comment deleted successfully.'), 'success')
                redirect_url = c.post_url
            else:
                comment.content = form['comment']
                model.session.commit()
                h.flash(_('Comment edited successfully.'), 'success')
                redirect_url = '%s#comment-%d' % (c.post_url, comment.id)
            redirect(redirect_url)
        except validators.Invalid, e:
            return h.htmlfill(e, form=post)

    @secure.authenticate_form
    def edit_post(self, post):
        try:
            form = PostForms().to_python(request.POST)
            if form['delete']:
                model.Comment.by_post(c.post.id).delete()
                model.Post.by_id(c.post.id).delete()
                model.session.commit()
                h.flash(_('Post deleted successfully.'), 'success')
                redirect_url = url(controller='blog', action='index')
            else:
                category_id = self.set_category(form)
                c.post.title = form['title']
                c.post.category_id = category_id
                c.post.content = form['content']
                c.post.user_id = c.user.id
                c.post.summary = form.get('summary', '')
                if form['slug'] != c.post.slug:
                    c.post.slug = self.set_slug(form)
                model.session.commit()
                h.flash(_('Post edited successfully.'), 'success')
                redirect_url = url(
                    controller='blog',
                    action='view',
                    category=c.post.category.slug,
                    slug=c.post.slug
                )
            redirect(redirect_url)
        except validators.Invalid, e:
            return h.htmlfill(e, form=post)

    @secure.authenticate_form
    def new_comment(self, post_form):
        remote_ip = h.getip()
        try:
            if c.user.id:
                form = CommentUserForm().to_python(request.POST)
                # Users do not have to pass any specific information.
                comment_kwargs = {'user_id': c.user.id}
            else:
                form = CommentForm().to_python(request.POST)
                comment_kwargs = {
                    'email': form['email'],
                    'url': form['url'],
                    'name': form['name']
                }
        except validators.Invalid, e:
            return h.htmlfill(e, form=post_form)
        # Use Akismet if a key has been provided to verify if a comment is
        # SPAM.  If it is marked as SPAM, then it will be hidden from view and
        # shown only to administrators, with the option of whether to approve
        # a comment or not.
        akismet_key = config.get('akismet.key', '')
        akismet_data = {
            'user_agent': request.environ.get('HTTP_USER_AGENT', ''),
            'user_ip': h.getip()
        }
        if akismet_key:
            akismet = Akismet(akismet_key)
            if akismet.comment_check(form['comment'], data=akismet_data):
                comment_args['spam'] = 1
                h.flash(
                    _('This comment has been marked for admin approval.'),
                    'warning'
                )
        # Finally, add the comment.
        comment = model.Comment(
            c.post.id,
            form['comment'],
            ip=remote_ip,
            **comment_kwargs
        )
        c.post.comments_count += 1
        model.session.add(comment)
        model.session.commit()
        redirect_url = '%s' % (url.current(),)
        if not comment.spam:
            redirect_url = u''.join(
                [redirect_url, '#comment-%s' % (comment.id,)]
            )
        redirect(redirect_url)

    @secure.authenticate_form
    def new_post(self):
        """Writing posts."""
        if not c.user.admin:
            abort(403)

        c.category_default = model.Category.first()
        post_write = render('post_write.tpl', slacks=True)

        if request.environ['REQUEST_METHOD'] != 'POST':
            return post_write

        try:
            form = PostForm().to_python(request.POST)
            category_id = self.set_category(form)
            slug = self.set_slug(form)
            post = model.Post(
                title=form['title'],
                category_id=category_id,
                content=form['content'],
                user_id=c.user.id,
                slug=slug,
                summary=form.get('summary', '')
            )
            model.session.add(post)
            model.session.commit()
            redirect_url = url(controller='blog', action='view',
                category=post.category.slug, slug=post.slug
            )
            redirect(redirect_url)
        except validators.Invalid, e:
            return h.htmlfill(e, form=post_write)

    def rss(self, posts):
        if not posts:
            h.flash('There are no posts to show an RSS Feed for.', 'warning')
            redirect(url(controller='blog', action='index'))

        author = model.User.first()
        host = request_config().host
        feed_kwargs = {}
        if author.email:
            feed_kwargs['author_email'] = author.email

        feed = Atom1Feed(
            title=config['rss.title'],
            description=config['rss.description'],
            link=url(host=host, controller='blog', action='index'),
            author_name=author.name,
            author_link=url(
                host=host,
                controller='account',
                action='profile',
                id=author.id
            ),
            **feed_kwargs
        )
        for post in c.posts:
            item_kwargs = {}
            if post.user.email:
                item_kwargs['author_email'] = post.user.email

            if post.summary:
                description = post.summary
            else:
                description = _('No Summary')

            feed.add_item(
                title=post.title,
                link=url(
                    host=host,
                    controller='blog',
                    action='view',
                    category=post.category.slug,
                    slug=post.slug
                ),
                description=description,
                pubdate=post.posted,
                author_name=post.user.name,
                author_link=url(
                    host=host,
                    controller='account',
                    action='profile',
                    id=post.user.id
                ),
                **item_kwargs
            )
        response.content_type = 'application/atom+xml'
        return feed.writeString('utf-8')

    def search(self):
        c.terms = request.GET.get('terms', '')
        c.results = []
        if len(c.terms) < 4:
            h.flash(
                _('Search queries must be at least 4 characters in length.'),
                'error'
            )
            redirect(url(controller='blog', action='index'))

        query = MultifieldParser(
            ['title', 'content', 'summary'],
            schema=index.schema
        ).parse(c.terms)
        results = index.searcher().search(query, limit=10)
        for result in results:
            terms = [v for k, v in query.all_terms() if k == 'content']
            url_kwargs = json.loads(result['url'])
            result['url'] = url(**url_kwargs)
            result['highlights'] = highlight(
                result['content'],
                terms,
                search.schema['content'].format.analyzer,
                ContextFragmenter(terms),
                HtmlFormatter(tagname='span', classname='highlight')
            )
            c.results.append(result)
        return render('search.tpl', slacks=True)

    def set_category(self, form):
        if form['category_title']:
            category = model.Category(form['category_title'])
            model.session.add(category)
            model.session.commit()
            return category.id
        else:
            try:
                return form['category_id']
            except KeyError:
                # If all else fails, fallback to the default category.
                return c.category_default

    def set_slug(self, form):
        try:
            model.Post.by_slug(form['slug']).one()
            h.flash(_('Slug already in use.'), 'error')
            return
        except NoResultFound:
            return form['slug']

    def view(self, category, slug='', edit=False, edit_comment=0):
        """Viewing of a post, category or page."""
        @cache.beaker_cache(**config['cache_options'])
        def load_post():
            post = model.Post.by_slug_category(slug, category).one()
            comments = post.comments
            return [post, comments]

        @cache.beaker_cache(**config['cache_options'])
        def load_category():
            _category = model.Category.by_slug(category).one()
            posts = _category.posts
            return [_category, posts]

        # If the slug is not specified, then it's a category.
        if not slug:
            return self.view_category(load_category, category, edit)
        else:
            try:
                c.post, c.comments = load_post()
            except (NoResultFound, AttributeError, ValueError):
                abort(404)
            return self.view_post(edit, edit_comment)

    def view_category(self, load_category, category, edit):
        try:
            c.category, c.posts = load_category()
            c.breadcrumbs.append({
                'title': c.category.title,
                'url': url(
                    controller='blog',
                    action='view',
                    category=c.category.slug
                )
            })

            c.editing = False
            if edit:
                if not c.user.admin:
                    abort(403)
                c.editing = True

            category_view = render('category.tpl', slacks=True)

            if request.environ['REQUEST_METHOD'] != 'POST':
                return category_view

            return self.edit_category(category_view)
        except (NoResultFound, ValueError):
            # There is no category, so our last option is that it's a
            # page.
            try:
                return render('content/%s.tpl' % (category,), slacks=True)
            except IOError:
                # There's no such page!
                abort(404)

    def view_post(self, edit, edit_comment):
        c.breadcrumbs.append({
            'title': c.post.category.title,
            'url': url(
                controller='blog',
                action='view',
                category=c.post.category.slug
            )
        })
        c.post_canedit = (c.user.id == c.post.user_id)
        c.post_url = url(controller='blog', action='view', 
            category=c.post.category.slug, slug=c.post.slug
        )
        c.editing_comment = 0
        c.editing_post = False

        if edit_comment:
            try:
                comment = model.Comment.by_id(edit_comment).one()
                if not (
                    c.user.id 
                    or c.user.id == comment.user_id
                    or c.user.admin
                ):
                    abort(403)
                c.editing_comment = edit_comment
            except NoResultFound:
                abort(404)
        elif edit:
            if not c.post_canedit:
                abort(403)
            c.category_default = model.Category.first()
            c.editing_post = True

        post = render('post.tpl', slacks=True)

        if request.environ['REQUEST_METHOD'] != 'POST':
            return post

        if edit:
            return self.edit_post(post)
        elif edit_comment:
            # We're editing a comment right now.
            return self.edit_comment(comment, post=post)
        else:
            # Allow the posting of comments.
            return self.new_comment(post)