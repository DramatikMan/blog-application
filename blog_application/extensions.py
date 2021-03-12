import datetime
from functools import wraps

from flask import flash, redirect, url_for, session, current_app
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
from flask_principal import Principal, Permission, RoleNeed
from flask_restful import Api
from celery import Celery


migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
principals = Principal()
rest_api = Api()

login_manager.login_view = 'main.login'
login_manager.session_protection = 'strong'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

admin_permission = Permission(RoleNeed('admin'))
poster_permission = Permission(RoleNeed('poster'))
default_permission = Permission(RoleNeed('default'))


def datetimeformat(value, format='%d-%m-%Y %H:%M'):
    return value.strftime(format)


def login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        '''
        This expands the original @login_required decorator logic
        in order to save the decorated function in the session object.
        '''
        session['ldf'] = {
            'name': func.__name__,
            'kwargs': kwargs
        }

        if not current_user.is_authenticated:
            return current_app.login_manager.unauthorized()

        session.pop('ldf', None)
        return func(*args, **kwargs)

    return decorated_view


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
