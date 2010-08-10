import logging

from pylons import config, request, response, session, tmpl_context as c, url
from pylons.controllers.util import redirect
from pylons.decorators import cache
from sqlalchemy.orm.exc import NoResultFound
from recaptcha.client import captcha
import formencode

from muse.lib import helpers as h
from muse.lib.base import _, BaseController, render
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
                posts = model.Post.get_all()
                return h.make_posts(posts)
            except NoResultFound:
                return
        c.posts = load_posts()
        return render('index.tpl', slacks=True)

    def view(self, category, id=''):
        """Viewing of a post, category or page."""
        @cache.beaker_cache(**cache_options)
        def load_post():
            post = model.Post.get_by_slug(id, category)
            comments = h.make_comments(post.comments)
            return [post, comments]

        @cache.beaker_cache(**cache_options)
        def load_category():
            _category = model.Category.get_by_id(category)
            posts = h.make_posts(_category.posts)
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
                    response.status = '404 Not Found'
                    return _('Page not found')
            return render('category.tpl', slacks=True)

        try:
            c.post, c.comments = load_post()
        except (NoResultFound, AttributeError, ValueError):
            response.status = '404 Not Found'
            return _('Post not found')

        c.recaptcha_error = ''
        post = render('post.tpl', slacks=True)

        if 'comment_add' in request.POST:
            remote_ip = h.get_ip()
            try:
                if c.user.id:
                    form = model.forms.CommentUser().to_python(request.params)
                    # Users do not have to pass any specific information.
                    comment_kwargs = {'user_id': c.user.id}
                else:
                    form = model.forms.Comment().to_python(request.params)
                    # XXX: Create a FormEncode validator for reCAPTCHA.
                    recaptcha_resp = captcha.submit(
                        form['recaptcha_challenge_field'],
                        form['recaptcha_response_field'],
                        config.get('recaptcha_private_key', ''),
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

            # Because the data that has to be entered varies by
            # whether or not one is a guest, the best option is for a
            # kwargs dict to
            # be passed.
            comment = model.Comment(c.post.id, form['comment'], ip=remote_ip,
                **comment_kwargs
            )
            model.session.add(comment)
            model.session.commit()
            # Redirect the user to the newly posted comment.
            redirect_url = url(controller='blog', action='view',
                id=c.post.slug, category=c.post.category.slug
            )
            redirect('%s#comment-%s' % (redirect_url, comment.id))
        return post