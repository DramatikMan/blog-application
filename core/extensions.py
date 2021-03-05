import flask
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_openid import OpenID
# from flask_oauth import OAuth
from flask_login import LoginManager
from flask_principal import Principal, Permission, RoleNeed
from flask_restful import Api
from celery import Celery


migrate = Migrate()
bcrypt = Bcrypt()
oid = OpenID()
# oauth = OAuth()
login_manager = LoginManager()
principals = Principal()
rest_api = Api()

login_manager.login_view = 'main.login'
login_manager.session_protection = 'strong'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_mesage_category = 'info'

admin_permission = Permission(RoleNeed('admin'))
poster_permission = Permission(RoleNeed('poster'))
default_permission = Permission(RoleNeed('default'))


@login_manager.user_loader
def load_user(user_id):
    from .models import User
    return User.query.get(user_id)


@oid.after_login
def create_or_login(resp):
    from .models import db, User
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


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

# facebook = oauth.remote_app(
#     'facebook',
#     base_url='https://graph.facebook.com',
#     request_token_url=None,
#     access_token_url='/oauth/access_token',
#     authorize_url='https://www.facebook.com/dialog/oauth',
#     consumer_key='',
#     consumer_secret='',
#     request_token_params={'scope': 'email'}
# )
#
# @facebook.tokengetter
# def get_facebook_auth_token():
#     return flask.session.get('facebook_oauth_token')
