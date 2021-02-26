import datetime

import flask
from sqlalchemy import text, func

from core.models import db, tags, User, Post, Comment, Tag
from core.forms import CommentForm


bp_blog = flask.Blueprint(
    'blog',
    __name__,
    template_folder=('../templates/blog'),
    url_prefix='/blog'
)


def sidebar_data():
    recent = Post.query.order_by(
        Post.publish_dt.desc()
    ).limit(5).all()
    top_tags = db.session.query(
        Tag, func.count(tags.c.post_id).label('total')
    ).join(
        tags
    ).group_by(Tag).order_by(text('total DESC')).limit(5).all()

    return recent, top_tags


@bp_blog.route('/')
@bp_blog.route('/<int:page>')
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


@bp_blog.route('/post/<int:post_id>', methods=['GET', 'POST'])
@bp_blog.route('/post/<int:post_id>/<int:page>', methods=['GET', 'POST'])
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


@bp_blog.route('/tag/<tag_name>')
@bp_blog.route('/tag/<tag_name>/<int:page>')
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


@bp_blog.route('/user/<username>')
@bp_blog.route('/user/<username>/<int:page>')
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
