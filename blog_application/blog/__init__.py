import os
import datetime

from flask import Blueprint, redirect, url_for, render_template, abort
from flask_login import current_user, login_required
from flask_principal import Permission, UserNeed
from sqlalchemy import text, func

from ..models import db, tags, User, Post, Comment, Tag
from ..forms import CommentForm, PostForm
from ..extensions import poster_permission, admin_permission


bp_blog = Blueprint(
    'blog',
    __name__,
    template_folder='templates/blog'
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


@bp_blog.route('/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()

    if form.validate_on_submit():
        new_post = Post(form.title.data)
        new_post.text = form.text.data
        new_post.publish_dt = datetime.datetime.now()
        new_post.user_id = current_user.get_id()

        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for('.post', post_id=new_post.id))

    return render_template('new.html', form=form)


@bp_blog.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@poster_permission.require(http_exception=403)
def edit_post(id):
    post = Post.query.get_or_404(id)
    if current_user != post.user:
        abort(403)

    permission = Permission(UserNeed(post.user.id))
    if permission.can() or admin_permission.can():
        form = PostForm()

        if form.validate_on_submit():
            post.title = form.title.data
            post.text = form.text.data
            post.publish_dt = datetime.datetime.now()

            db.session.add(post)
            db.session.commit()

            return redirect(url_for('.post', post_id=post.id))

        form.text.data = post.text
        return render_template('edit.html', form=form, post=post)
    else:
        abort(403)


@bp_blog.route('/')
@bp_blog.route('/<int:page>')
def home(page=1):
    posts = Post.query.order_by(
        Post.publish_dt.desc()
    ).paginate(page, 10)
    recent, top_tags = sidebar_data()

    return render_template(
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

        return redirect(str(post_id))

    post = Post.query.get_or_404(post_id)
    tags = post.tags
    comments = post.comments.order_by(Comment.dt.desc()).paginate(page, 10)
    recent, top_tags = sidebar_data()

    return render_template(
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

    return render_template(
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

    return render_template(
        'user.html',
        user=user,
        posts=posts,
        recent=recent,
        top_tags=top_tags
    )
