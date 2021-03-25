import os

from flask import current_app
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from flask_login import AnonymousUserMixin
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature
from itsdangerous import SignatureExpired

from .extensions import bcrypt, login_manager


schema = 'test' if os.environ['FLASK_ENV'] == 'testing' else 'public'
db = SQLAlchemy(metadata=MetaData(schema=schema))


tags = db.Table('post_x_tags',
    db.Column('post_id', db.Integer(), db.ForeignKey('post.id')),
    db.Column('tag_id', db.Integer(), db.ForeignKey('tag.id')),
    db.UniqueConstraint('post_id', 'tag_id')
)
roles = db.Table('user_x_role',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
    db.UniqueConstraint('user_id', 'role_id')
)


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255))
    email = db.Column(db.String(256), unique=True)
    posts = db.relationship(
        'Post',
        backref='user',
        lazy='dynamic'
    )
    roles = db.relationship(
        'Role',
        secondary=roles,
        backref=db.backref('users', lazy='dynamic')
    )

    def __init__(self, username, email=None, password=None):
        self.username = username
        self.email = email
        self.password = password
        default = Role.query.filter_by(name='default').one()
        poster = Role.query.filter_by(name='poster').one()
        self.roles = [default, poster]

    def __repr__(self):
        return f"<User '{self.username}'>"

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode()

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def is_authenticated(self):
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True

    def is_active(self):
        return True

    def is_anonymous(self):
        if isinstance(self, AnonymousUserMixin):
            return True
        else:
            return False

    def get_id(self):
        return self.id

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])

        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None

        user = User.query.get(data['id'])
        return user


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class OAuth(OAuthConsumerMixin, db.Model):
    provider_user_id = db.Column(db.String(256), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    user = db.relationship('User', backref='oauth')


class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255))
    text = db.Column(db.Text())
    publish_dt = db.Column(db.DateTime())
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    comments = db.relationship('Comment', backref='post', lazy='dynamic')
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
    post_id = db.Column(db.Integer(), db.ForeignKey(Post.id))

    def __repr__(self):
        return f"<Comment '{self.text[:15]}'>"


class Tag(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255), unique=True)

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return f"<Tag '{self.title}'>"


class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<Role '{self.name}'>"
