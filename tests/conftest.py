import pytest

from blog_application import create_app
from blog_application.commands import db_fill, db_clear


@pytest.fixture(scope='session')
def app():
    app = create_app()
    cli = app.test_cli_runner()
    cli.invoke(db_fill)
    yield app

    cli.invoke(db_clear)


@pytest.fixture(scope='session')
def client(app):
    return app.test_client()


@pytest.fixture(scope='session')
def runner(app):
    return app.test_cli_runner()
