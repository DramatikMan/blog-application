from flask_sqlalchemy import SQLAlchemy

from core.extensions import bcrypt


db = SQLAlchemy()


tags = db.Table('post_x_tags',
    db.Column('post_id', db.Integer(), db.ForeignKey('post.id')),
    db.Column('tag_id', db.Integer(), db.ForeignKey('tag.id'))
)


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255))

    posts = db.relationship(
        'Post',
        backref='user',
        lazy='dynamic'
    )

    def __init__(self, username, password=None):
        self.username = username
        self.password = password

    def __repr__(self):
        return f"<User '{self.username}'>"

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode()

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)


class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255))
    text = db.Column(db.Text())
    publish_dt = db.Column(db.DateTime())

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    comments = db.relationship(
        'Comment',
        backref='post',
        lazy='dynamic'
    )

    tags = db.relationship(
        'Tag',
        secondary=tags,
        backref=db.backref('posts', lazy='dynamic')
    )

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return f"<Post '{self.title}'>"


class Comment(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255))
    text = db.Column(db.Text())
    dt = db.Column(db.DateTime())

    post_id = db.Column(db.Integer(), db.ForeignKey('post.id'))

    def __repr__(self):
        return f"<Comment '{self.text[:15]}'>"


class Tag(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255), unique=True)

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return f"<Tag '{self.title}'>"
