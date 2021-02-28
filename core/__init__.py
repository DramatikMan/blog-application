import os

import flask

from core.extensions import migrate, bcrypt, oid
from core.models import db, tags, User, Post, Comment, Tag
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

    # flask CLI utility
    app.register_blueprint(cmd)

    app.register_blueprint(bp_main)
    app.register_blueprint(bp_blog)

    # flask shell utility
    @app.shell_context_processor
    def make_shell_context():
        return dict(
            app=app,
            db=db,
            tags=tags,
            User=User,
            Post=Post,
            Comment=Comment,
            Tag=Tag
        )

    return app
