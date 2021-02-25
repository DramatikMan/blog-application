import os

import flask
from flask_migrate import Migrate

from core.models import db, tags, User, Post, Comment, Tag
from core.commands import cmd
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
    migrate = Migrate(app, db)

    @app.route('/')
    def index():
        return flask.redirect(flask.url_for('blog.home'))

    app.register_blueprint(cmd)
    app.register_blueprint(bp_blog)

    @app.shell_context_processor
    def make_shell_context():
        return dict(
            app=app,
            db=db,
            User=User,
            Post=Post,
            Comment=Comment,
            tags=tags,
            Tag=Tag
        )

    return app
