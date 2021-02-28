import os

import flask
from flask_login import current_user
from flask_principal import identity_loaded, UserNeed, RoleNeed

from core.extensions import migrate, bcrypt, oid, login_manager, principals
from core.models import db, tags, roles, User, Post, Comment, Tag, Role
from core.commands import cmd
from core.controllers.main import bp_main
from core.controllers.blog import bp_blog


def create_app():
    app = flask.Flask(__name__)

    if os.environ.get('FLASK_ENV') == 'production':
        cfg = 'ProdConfig'
    elif os.environ.get('FLASK_ENV') == 'development':
        cfg = 'DevConfig'

    app.config.from_object('config.' + cfg)
    app.url_map.strict_slashes = False

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    oid.init_app(app)
    login_manager.init_app(app)
    principals.init_app(app)

    # flask CLI utility
    app.register_blueprint(cmd)
    # module blueprints
    app.register_blueprint(bp_main)
    app.register_blueprint(bp_blog)

    # flask shell utility
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
        # set the indentity user object
        identity.user = current_user

        # add the UserNeed to the identity
        if hasattr(current_user, 'id'):
            identity.provides.add(UserNeed(current_user.id))

        # add each role to the identity
        if hasattr(current_user, 'roles'):
            for role in current_user.roles:
                identity.provides.add(RoleNeed(role.name))

    return app
