import os

import pytest

from blog_application import create_app
from blog_application.models import db, User, Post, Tag, Role
from blog_application.commands import db_fill


@pytest.fixture(scope='session')
def client():
    app = create_app()
    with app.test_client() as client:
        yield client
