import logging

from pylons import config, request, response, session, tmpl_context as c, url
from pylons.decorators import rest, validate
from pylons.controllers.util import abort, redirect
from sqlalchemy.orm.exc import NoResultFound
from openid.consumer.consumer import Consumer
from openid.extensions.sreg import SRegRequest, SRegResponse
from openid.store.filestore import FileOpenIDStore
from openid.yadis.discover import DiscoveryFailure
from routes import request_config

from muse.lib.base import _, BaseController, render
from muse.lib.decorators import require
from muse.lib import helpers as h
from muse import model

log = logging.getLogger(__name__)

class AccountController(BaseController):
    """Most of this is ported from the users controller from Parasol Boards,
    seeing as both seem to accomplish the same thing.
    """

    openid_store = FileOpenIDStore('/var/tmp')

    def index(self):
        redirect(url(controller='blog', action='index'))

    def openid(self):
        return render('account/openid.tpl', slacks=True)

    @require('guest')
    @validate(schema=model.forms.Login(), form='what_is_openid')
    def login(self):
        try:
            openid_url = self.form_result['openid_identifier']
        except (AttributeError):
            redirect(url(controller='blog', action='index'))
        cons = Consumer(session=session, store=self.openid_store)
        try:
            auth_request = cons.begin(openid_url)
            sreg_request = SRegRequest(optional=['nickname', 'email', 'gender',
                'country', 'language', 'timezone'])
            auth_request.addExtension(sreg_request)
            host = request.headers['host']
            protocol = request_config().protocol
            return_url = url(host=host, controller='account',
                action='login_complete')
            new_url = auth_request.redirectURL(return_to=return_url,
                realm='%s://%s' % (protocol, host))
            session['redirect_url'] = request.environ.get('HTTP_REFERER',
                url(controller='blog', action='index'))
            session.save()
            redirect(new_url)
        except DiscoveryFailure:
            return _('No usable OpenID provider found.')

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
            user = model.User(name=name, email=email,
                identifier=result.identity_url
            )
            model.session.add(user)
            model.session.commit()
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