import flask
from flask_migrate import Migrate

from config import DevConfig
import database
from commands import cmd
from models import *


app = flask.Flask(__name__)

app.config.from_object(DevConfig)
app.url_map.strict_slashes = False

database.init_app(app)
app.register_blueprint(cmd)
migrate = Migrate(app, database.db)


@app.route('/')
@app.route('/<int:page>')
def home(page=1):
    posts = Post.query.order_by(
        Post.publish_dt.desc()
    ).paginate(page, 10)
    recent, top_tags = sidebar_data()

    return flask.render_template(
        'home.html',
        posts=posts,
        recent=recent,
        top_tags=top_tags
    )


@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    tags = post.tags
    comments = post.comments.order_by(Comment.dt.desc()).all()
    recent, top_tags = sidebar_data()

    return flask.render_template(
        'post.html',
        post=post,
        tags=tags,
        comments=comments,
        recent=recent,
        top_tags=top_tags
    )


@app.route('/tag/<tag_name>')
def tag(tag_name):
    tag = Tag.query.filter_by(title=tag_name).first_or_404()
    posts = tag.posts.order_by(Post.publish_dt.desc()).all()
    recent, top_tags = sidebar_data()

    return flask.render_template(
        'tag.html',
        tag=tag,
        posts=posts,
        recent=recent,
        top_tags=top_tags
    )


@app.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts.order_by(Post.publish_dt.desc()).all()
    recent, top_tags = sidebar_data()

    return render_template(
        'user.html',
        user=user,
        posts=posts,
        recent=recent,
        top_tags=top_tags
    )


if __name__ == '__main__':
    app.run()
