import random
import datetime
import click

from flask import Blueprint

from .models import db, User, Post, Tag, Role


cmd = Blueprint('cmd', __name__, cli_group=None)


@cmd.cli.command('db_clear')
@click.argument('all')
def db_drop_all(all):
    '''Drop all tables from the connected database.'''
    db.drop_all()


@cmd.cli.command('db_fill')
@click.argument('all')
def db_fill_all(all):
    '''Create all tables and fill them with example data.'''
    db.create_all()

    role_1 = Role('admin')
    role_2 = Role('poster')
    role_3 = Role('default')
    db.session.bulk_save_objects([role_1, role_2, role_3])

    user = User(username='DramatikMan')
    user.set_password('SilenceAndSleep')
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
