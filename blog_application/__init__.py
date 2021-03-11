import os

import flask
from flask_login import current_user
from flask_principal import identity_loaded, UserNeed, RoleNeed
from sqlalchemy import event

# from .extensions import migrate
from .extensions import bcrypt
from .extensions import oid
from .extensions import login_manager
from .extensions import principals
# from .extensions import rest_api+
from .extensions import make_celery

from .extensions import datetimeformat

from .models import db, tags, roles, User, Post, Comment, Tag, Role, Reminder

from .commands import bp_cmd
from .blog import bp_blog
from .main import bp_main

from .api import rest_api
from .tasks import on_reminder_save


if os.environ.get('FLASK_ENV') == 'production':
        cfg = 'ProdConfig'
elif os.environ.get('FLASK_ENV') == 'development':
        cfg = 'DevConfig'
elif os.environ.get('FLASK_ENV') == 'testing':
        cfg = 'TestConfig'


def create_app():
    app = flask.Flask(__name__)

    app.config.from_object('config.' + cfg)
    app.url_map.strict_slashes = False

    '''database resources'''
    db.init_app(app)
    event.listen(Reminder, 'after_insert', on_reminder_save)

    '''jinja custom filters'''
    app.jinja_env.filters['datetimeformat'] = datetimeformat

    '''extensions'''
    # migrate.init_app(app, db)
    bcrypt.init_app(app)
    oid.init_app(app)
    login_manager.init_app(app)
    principals.init_app(app)
    rest_api.init_app(app)
    celery = make_celery(app)

    '''module blueprints'''
    app.register_blueprint(bp_blog)
    app.register_blueprint(bp_cmd)
    app.register_blueprint(bp_main)

    '''flask shell utility'''
    @app.shell_context_processor
    def make_shell_context():
        return dict(
            app=app,
            db=db,
            tags=tags,
            roles=roles,
            User=User,
            Post=Post,
            Comment=Comment,
            Tag=Tag,
            Role=Role
        )

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        '''set the indentity user object'''
        identity.user = current_user

        '''add the UserNeed to the identity'''
        if hasattr(current_user, 'id'):
            identity.provides.add(UserNeed(current_user.id))

        '''add each role to the identity'''
        if hasattr(current_user, 'roles'):
            for role in current_user.roles:
                identity.provides.add(RoleNeed(role.name))

    return app
