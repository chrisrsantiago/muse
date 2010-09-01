import logging

from pylons import config, request, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons.decorators import cache
from sqlalchemy.orm.exc import NoResultFound
from recaptcha.client import captcha
import formencode

from muse.lib.base import _, BaseController, h, render
from muse import model

log = logging.getLogger(__name__)
cache_options = {
    'query_args': True,
    'expire': config['cache_expire'],
    'invalidate_on_startup': True
}

class BlogController(BaseController):
    
    def index(self):
        """The default page is loaded, as no post has been specified."""
        @cache.beaker_cache(**cache_options)
        def load_posts():
            try:
                return model.Post.all()
            except NoResultFound:
                return
        c.posts = load_posts()
        return render('index.tpl', slacks=True)

    def new_category(self):
        pass

    def new_post(self):
        """Writing posts."""
        if not c.user.admin:
            abort(403)

        c.category_default = model.Category.first()
        post_write = render('post_write.tpl', slacks=True)

        if request.environ['REQUEST_METHOD'] != 'POST':
            return post_write

        try:
            form = model.forms.Post().to_python(request.POST)

            try:
                # Make the new category
                category = model.Category(form['category_title'])
                model.session.add(category)
                model.session.commit()
                category_id = category.id
            except KeyError:
                try:
                    category_id = form['category_id']
                except KeyError:
                    # If all else fails, fallback to the default category.
                    category_id = c.category_default.id

            post = model.Post(
                title=form['title'],
                category_id=category_id,
                content=form['content'],
                author_id=c.user.id,
                slug=form['slug'],
                summary=form.get('summary', '')
            )
            model.session.add(post)
            model.session.commit()
            redirect_url = url(controller='blog', action='view',
                category=post.category.slug, id=post.slug
            )
            redirect(redirect_url)
        except formencode.validators.Invalid, e:
            return h.htmlfill(e, form=post_write)

    def view(self, category, id=''):
        """Viewing of a post, category or page."""
        @cache.beaker_cache(**cache_options)
        def load_post():
            post = model.Post.by_slug_category(id, category)
            comments = post.comments
            return [post, comments]

        @cache.beaker_cache(**cache_options)
        def load_category():
            _category = model.Category.by_slug(category)
            posts = _category.posts
            return [_category, posts]

        # If the ID is not specified, then it's a category.
        if not id:
            try:
                c.category, c.posts = load_category()
            except (NoResultFound, ValueError):
                # There is no category, so our last option is that it's a
                # page.
                try:
                    return render('content/%s.tpl' % (category,), slacks=True)
                except IOError:
                    # There's no such page!
                    abort(404)
            return render('category.tpl', slacks=True)

        try:
            c.post, c.comments = load_post()
        except (NoResultFound, AttributeError, ValueError):
            abort(404)

        post = render('post.tpl', slacks=True)

        if request.environ['REQUEST_METHOD'] != 'POST':
            return post

        remote_ip = h.getip()
        try:
            if c.user.id:
                form = model.forms.CommentUser().to_python(request.params)
                # Users do not have to pass any specific information.
                comment_kwargs = {'user_id': c.user.id}
            else:
                form = model.forms.Comment().to_python(request.params)
                recaptcha_resp = captcha.submit(
                    form['recaptcha_challenge_field'],
                    form['recaptcha_response_field'],
                    config.get('recaptcha.private_key', ''),
                    remote_ip
                )
                comment_kwargs = {
                    'email': form['email'],
                    'url': form['url'],
                    'name': form['name']
                }
                if not recaptcha_resp.is_valid:
                    c.recaptcha_error = (recaptcha_resp.is_valid)
                    return post
        except formencode.validators.Invalid, e:
            return h.htmlfill(e, form=post)

        comment = model.Comment(c.post.id, form['comment'], ip=remote_ip,
            **comment_kwargs
        )
        c.post.comments_count += 1
        model.session.add(comment)
        model.session.commit()
        # Redirect the user to the newly posted comment.
        redirect_url = url(controller='blog', action='view',
            id=c.post.slug, category=c.post.category.slug
        )
        redirect('%s#comment-%s' % (redirect_url, comment.id))