import datetime
import flask
from flask_migrate import Migrate

from config import DevConfig
from database import *
from commands import cmd
from models import *
from forms import *


app = flask.Flask(__name__)

app.config.from_object(DevConfig)
app.url_map.strict_slashes = False

init_app(app)
app.register_blueprint(cmd)
migrate = Migrate(app, db)


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


@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
@app.route('/post/<int:post_id>/<int:page>', methods=['GET', 'POST'])
def post(post_id, page=1):
    form = CommentForm()
    if form.validate_on_submit():
        new_comment = Comment()
        new_comment.name = form.name.data
        new_comment.text = form.text.data
        new_comment.post_id = post_id
        new_comment.dt = datetime.datetime.now()
        db.session.add(new_comment)
        db.session.commit()
        return flask.redirect(str(post_id))

    post = Post.query.get_or_404(post_id)
    tags = post.tags
    comments = post.comments.order_by(Comment.dt.desc()).paginate(page, 10)
    recent, top_tags = sidebar_data()

    return flask.render_template(
        'post.html',
        post=post,
        tags=tags,
        comments=comments,
        recent=recent,
        top_tags=top_tags,
        form=form
    )


@app.route('/tag/<tag_name>')
@app.route('/tag/<tag_name>/<int:page>')
def tag(tag_name, page=1):
    tag = Tag.query.filter_by(title=tag_name).first_or_404()
    posts = tag.posts.order_by(Post.publish_dt.desc()).paginate(page, 10)
    recent, top_tags = sidebar_data()

    return flask.render_template(
        'tag.html',
        tag=tag,
        posts=posts,
        recent=recent,
        top_tags=top_tags
    )


@app.route('/user/<username>')
@app.route('/user/<username>/<int:page>')
def user(username, page=1):
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts.order_by(Post.publish_dt.desc()).paginate(page, 10)
    recent, top_tags = sidebar_data()

    return flask.render_template(
        'user.html',
        user=user,
        posts=posts,
        recent=recent,
        top_tags=top_tags
    )


if __name__ == '__main__':
    app.run()
