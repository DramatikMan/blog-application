import random
import datetime
import click

from flask import Blueprint, current_app

from ..models import db, User, Post, Tag, Role


bp_cmd = Blueprint('cmd', __name__, cli_group=None)


@bp_cmd.cli.command('db_clear')
def db_clear():
    '''Drop all tables from the connected database.'''
    db.drop_all()


@bp_cmd.cli.command('db_fill')
def db_fill():
    '''Create all tables and fill them with example data.'''
    db.create_all()

    role_1 = Role('admin')
    role_2 = Role('poster')
    role_3 = Role('default')
    db.session.bulk_save_objects([role_1, role_2, role_3])

    user = User(
        username=current_app.config['ADMIN_NAME'],
        email=current_app.config['ADMIN_EMAIL']
    )
    user.set_password(current_app.config['ADMIN_PASSWORD'])
    admin = Role.query.filter_by(name='admin').one()
    user.roles.append(admin)
    db.session.add(user)

    tag_one = Tag('Python')
    tag_two = Tag('Flask')
    tag_three = Tag('SQLAlchemy')
    tag_four = Tag('Jinja')
    tag_list = [tag_one, tag_two, tag_three, tag_four]

    for i in range(100):
        new_post = Post('Post ' + str(i + 1))
        new_post.user = user
        new_post.publish_dt = datetime.datetime.now() + datetime.timedelta(seconds=i)
        new_post.text = 'Example text'
        new_post.tags = random.sample(tag_list, random.randint(1, 3))
        db.session.add(new_post)

    db.session.commit()
