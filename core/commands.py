import click

from flask import Blueprint

import core.models as models


cmd = Blueprint('cmd', __name__, cli_group=None)


@cmd.cli.command('create_table')
@click.argument('model_class')
def create_table(model_class):
    '''Create a new table for the specified model class.'''
    getattr(models, model_class).__table__.create(models.db.engine)


@cmd.cli.command('drop_table')
@click.argument('model_class')
def drop_table(model_class):
    '''Drop the specified model class's corresponding table.'''
    getattr(models, model_class).__table__.drop(models.db.engine)
