import logging

from pylons import config, request, session, tmpl_context as c, url
from pylons.decorators import rest, validate
from pylons.controllers.util import abort, redirect
from routes import request_config
import elixir
from sqlalchemy.orm.exc import NoResultFound
from openid.consumer.consumer import Consumer
from openid.extensions.sreg import SRegRequest, SRegResponse
from openid.store.filestore import FileOpenIDStore
import formencode

from muse.lib.base import _, BaseController, h, render
from muse.lib.decorators import require
from muse import model

log = logging.getLogger(__name__)

class AccountController(BaseController):
    openid_store = FileOpenIDStore('/var/tmp')

    def index(self):
        # XXX: Until I make a member's area or something like that.
        redirect(url(controller='blog', action='index'))

    @require('guest')
    def login(self):
        login = render('account/login.tpl', slacks=True)

        if request.environ['REQUEST_METHOD'] != 'POST':
            return login

        try:
            form = model.forms.Login().to_python(request.params)            
        except formencode.validators.Invalid, e:
            return h.htmlfill(e, form=login)

        cons = Consumer(session=session, store=self.openid_store)
        auth_request = cons.begin(form['openid_identifier'])
        auth_request.addExtension(SRegRequest(optional=[
            'nickname', 'email'
        ]))
        host = request.headers['host']
        realm = '%s://%s' % (request_config().protocol, host)
        return_url = url(
            host=host, controller='account', action='login_complete'
        )
        new_url = auth_request.redirectURL(
            return_to=return_url, realm=realm
        )
        session['redirect_url'] = request.environ.get(
            'HTTP_REFERER', url(controller='blog', action='index')
        )
        session.save()
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
            user = model.User.get_by_identifier(result.identity_url)
            session['userid'] = user.id
        except (AttributeError, NoResultFound):
            # No previous login record for the user.
            sreg_res = SRegResponse.fromSuccessResponse(result)
            try:
                email = sreg_res['email']
            except TypeError, KeyError:
                email = ''

            if sreg_res and 'nickname' in sreg_res:
                name = sreg_res['nickname']
            else:
                name = result.identity_url
            user = model.User(name=name, identifier=result.identity_url,
                email=email
            )
            elixir.session.add(user)
            elixir.session.commit()
            session['userid'] = user.id
        session.save()
        redirect_url = session.get('redirect_url',
            url(controller='blog', action='index')
        )
        # Prevent sending the user to the login page again because you
        # shall be denied permission otherwise.
        if 'login' in redirect_url:
            redirect_url = url(controller='blog', action='index')
        redirect(redirect_url)

    @require('member')
    def logout(self):
        try:
            del session['userid']
            session.save()
        except KeyError:
            pass
        redirect(url(controller='blog', action='index'))