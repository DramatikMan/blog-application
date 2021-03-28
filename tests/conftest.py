import pytest
from sqlalchemy import text

from blog_application import create_app
from blog_application.commands import db_fill, db_clear
from blog_application.models import db


@pytest.fixture(scope='session')
def app():
    app = create_app()
    with app.app_context():
        db.engine.execute(text('CREATE SCHEMA IF NOT EXISTS test'))
    cli = app.test_cli_runner()
    cli.invoke(db_clear)
    cli.invoke(db_fill)
    yield app

    cli.invoke(db_clear)


@pytest.fixture(scope='session')
def client(app):
    return app.test_client()


@pytest.fixture(scope='session')
def runner(app):
    return app.test_cli_runner()
