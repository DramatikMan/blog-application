import os

from flask import Flask
from flask_login import current_user
from flask_principal import identity_loaded, UserNeed, RoleNeed

from .extensions import (
    migrate,
    bcrypt,
    login_manager,
    principals,
    datetimeformat
)
from .api import rest_api
from .models import db, tags, roles, User, Post, Comment, Tag, Role
from .commands import bp_cmd
from .blog import bp_blog
from .main import bp_main
from .api import bp_api
from .oauth.google import bp_google


def create_app():
    app = Flask(__name__)

    cfg = f"config.{os.environ.get('FLASK_ENV').capitalize()}Config"
    app.config.from_object(cfg)
    app.url_map.strict_slashes = False
    app.jinja_env.filters['datetimeformat'] = datetimeformat

    db.init_app(app)

    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    principals.init_app(app)
    rest_api.init_app(app)

    app.register_blueprint(bp_cmd)
    app.register_blueprint(bp_blog, url_prefix='/blog')
    app.register_blueprint(bp_main)
    app.register_blueprint(bp_api, url_prefix='/api')
    app.register_blueprint(bp_google)

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
