import os
import logging

from pylons import config, request, session, tmpl_context as c, url
from pylons.decorators import cache
from pylons.controllers.util import abort, redirect
from routes import request_config
from sqlalchemy.orm.exc import NoResultFound
from openid.consumer.consumer import Consumer
from openid.yadis.discover import DiscoveryFailure
from openid.extensions.sreg import SRegRequest, SRegResponse
from openid.store.filestore import FileOpenIDStore
from formencode import validators, Schema
from pygeoip import GeoIP

from muse.lib.base import _, BaseController, h, render
from muse.lib.decorators import require
from muse import model

log = logging.getLogger(__name__)

class LoginForm(Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    openid_identifier = validators.OpenId(not_empty=True)


class ProfileForm(Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    delete = validators.StringBoolean(if_missing=False)
    identifier = validators.OpenId(not_empty=True)
    name = validators.UnicodeString(not_empty=True, strip=True)
    email = validators.Email(not_empty=False, resolve_domain=True)
    website = validators.URL(add_http=True)


class AccountController(BaseController):
    geoip = GeoIP(os.path.join(config['pylons.paths']['data'], 'geoip.dat'))
    openid_store = FileOpenIDStore('/var/tmp')

    @require('guest')
    def login(self):
        login = render('account/login.tpl', slacks=True)

        if request.environ['REQUEST_METHOD'] != 'POST':
            return login

        try:
            form = LoginForm().to_python(request.POST)            
        except validators.Invalid, e:
            return h.htmlfill(e, form=login)

        try:
            cons = Consumer(session=session, store=self.openid_store)
            auth_request = cons.begin(form['openid_identifier'])
            auth_request.addExtension(SRegRequest(optional=[
                'nickname',
                'email'
            ]))
        except DiscoveryFailure:
            h.flash(
                _('The specified URL is not a valid OpenID end-point.'),
                'error'
            )
            redirect(url(controller='account', action='login'))
        host = request.headers['host']
        realm = '%s://%s' % (request_config().protocol, host)
        return_url = url(
            host=host, controller='account', action='login_complete'
        )
        new_url = auth_request.redirectURL(return_to=return_url, realm=realm)
        redirect(new_url)

    @require('guest')
    def login_complete(self):
        """This function is called once a user has succesfully logged in to
        his/her OpenID account. The user is then prompted to choose a
        preferred alias to be known as if a default one is not provided.
        """
        consumer = Consumer(session=session, store=self.openid_store)
        host = request.headers['host']
        return_url = url(host=host, controller='account',
            action='login_complete')
        result = consumer.complete(request.params, return_url)
        if result.status != 'success':
            return _('An error ocurred with login.')
        try:
            user = model.User.by_identifier(result.identity_url).one()
            session['userid'] = user.id
        except (AttributeError, NoResultFound):
            # No previous login record for the user.
            sreg_res = SRegResponse.fromSuccessResponse(result)
            try:
                email = sreg_res['email']
            except (TypeError, KeyError):
                email = ''

            try:
                name = sreg_res['nickname']
            except (TypeError, KeyError):
                name = result.identity_url
            user = model.User(
                name=name,
                identifier=result.identity_url,
                email=email
            )
            try:
                model.User.all()
            except NoResultFound:
                # Since you're going to be the only user, might as well grant
                # you administrator privileges.
                user.admin = True
            model.session.add(user)
            model.session.commit()
            session['userid'] = user.id
        session.save()
        if user.name == result.identity_url:
            h.flash(
                _('Login was successful, but now you need to set a name.'),
                'warning'
            )
            redirect(
                url(
                    controller='account',
                    action='profile',
                    id=user.id,
                    edit='true'
                )
            )
        redirect(url(controller='blog', action='index'))

    @require('member')
    def logout(self):
        try:
            del session['userid']
            session.save()
        except KeyError:
            pass
        redirect(url(controller='blog', action='index'))

    def profile(self, id='', edit=''):
        @cache.beaker_cache(**config['cache_options'])
        def get_user():
            return model.User.by_id(id).one()

        @cache.beaker_cache(**config['cache_options'])
        def get_users():
            return model.User.all()

        if not id:
            try:
                c.profiles = get_users()
            except NoResultFound:
                c.profiles = []
            return render('account/profiles.tpl', slacks=True)

        try:
            c.profile = get_user()
        except NoResultFound:
            abort(404)
        c.breadcrumbs.append({
            'title': _('Users List'),
            'url': url(controller='account', action='profile')
        })
        c.canedit = (c.user.admin or c.user.id == c.profile.id)
        c.editing = False
        if edit:
            if c.canedit:
                c.editing = True
                c.breadcrumbs.append({
                    'title': _('Editing'),
                    'url': ''
                })
            else:
                abort(403)

        sorted(c.profile.comments, reverse=True)
        try:
            c.country = self.geoip.country_code_by_addr(c.profile.ip).lower()
        except AttributeError:
            c.country = ''
        c.comments = c.profile.comments[:5]
        c.comments_count = len(c.profile.comments)
        c.posts_count = len(c.profile.posts)
        profile_page = render('account/profile.tpl', slacks=True)

        if not request.environ['REQUEST_METHOD'] == 'POST':
            return profile_page

        try:
            form = ProfileForm().to_python(request.POST)
            # Only administrators can delete users.
            if form['delete'] and c.user.admin:
                # Delete all posts, comments and finally the profile for this
                # user if checkbox is ticked.
                model.Post.by_user(c.profile.id).delete()
                model.Comment.by_user(c.profile.id).delete()
                model.User.by_id(c.profile.id).delete()
                model.session.commit()
                h.flash(_('User has been deleted.'), 'success')
                redirect_url = url(controller='blog', action='index')
            else:
                if form['name'] != c.profile.name:
                    try:
                        model.User.by_name(form['name']).one()
                        h.flash(_('Username Taken'), 'error')
                    except NoResultFound:
                        c.profile.name = form['name']

                c.profile.email = form['email']
                c.profile.identifier = form['identifier']
                c.profile.website = form['website']
                model.session.commit()
                h.flash(_('Profile Updated'), 'success')
                redirect_url = url(
                    controller='account',
                    action='profile',
                    id=c.profile.id
                )
            redirect(redirect_url)
        except validators.Invalid, e:
            return h.htmlfill(e, profile_page)

        return profile_page