from blog_application.models import Comment
from .utils import login, logout


def test_home(client):
    response = client.get('/blog')
    assert response.status_code == 200
    assert b'Recent Posts' in response.data
    assert b'Popular Tags' in response.data


def test_post_page(client):
    response = client.get('/blog/post/100')
    assert response.status_code == 200
    assert b'Written by' in response.data
    assert b'New comment' in response.data


def test_add_comment(app, client):
    payload = dict(name='tester', text='Example comment')
    client.post('/blog/post/100', data=payload)
    with app.app_context():
        added_comment = Comment.query.filter_by(text='Example comment').first()
    assert added_comment


def test_user_page(client):
    response = client.get('/blog/user/Random_User')
    assert response.status_code == 200
    assert b'Posts by author: Random_User' in response.data
    assert b'First' in response.data


def test_tag_page(client):
    response = client.get('/blog/tag/Flask')
    assert response.status_code == 200
    assert b'Posts by tag: &laquo;Flask&raquo;' in response.data
    assert b'First' in response.data
