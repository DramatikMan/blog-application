import flask
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_openid import OpenID
# from flask_oauth import OAuth
from flask_login import LoginManager
from flask_principal import Principal, Permission, RoleNeed


migrate = Migrate()
bcrypt = Bcrypt()
oid = OpenID()
# oauth = OAuth()
login_manager = LoginManager()
principals = Principal()

login_manager.login_view = 'main.login'
login_manager.session_protection = 'strong'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_mesage_category = 'info'

admin_permission = Permission(RoleNeed('admin'))
poster_permission = Permission(RoleNeed('poster'))
default_permission = Permission(RoleNeed('default'))


@login_manager.user_loader
def load_user(user_id):
    from core.models import User
    return User.query.get(user_id)


@oid.after_login
def create_or_login(resp):
    from core.models import db, User
    username = resp.fullname or resp.nickname or resp.email
    if not username:
        flask.flash('Invalid login. Please try again.', 'danger')
        return flask.redirect(flask.url_for('main.login'))

    user = User.query.filter_by(username=username).first()
    if user is None:
        user = User(username)
        db.session.add(user)
        db.session.commit()

    return flask.redirect(flask.url_for('blog.home'))


# facebook = oauth.remote_app(
#     'facebook',
#     base_url='https://graph.facebook.com',
#     request_token_url=None,
#     access_token_url='/oauth/access_token',
#     authorize_url='https://www.facebook.com/dialog/oauth',
#     consumer_key='2483573918454846',
#     consumer_secret='b8734f6bc4a4bc359ef5ee13f8f1476a',
#     request_token_params={'scope': 'email'}
# )
#
# @facebook.tokengetter
# def get_facebook_auth_token():
#     return flask.session.get('facebook_oauth_token')
