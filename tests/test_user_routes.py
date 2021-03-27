from blog_application.models import Post
# from blog_application.forms import PostForm
from .utils import login, logout


def test_login_logout(client):
    response = login(client, 'Random_User', 'no_brute_force_please')
    assert b'You have been logged in.' in response.data

    response = logout(client)
    assert b'You have been logged out.' in response.data

    response = login(client, 'Random_User' + 'x', 'no_brute_force_please')
    assert b'Invalid username or password' in response.data

    response = login(client, 'Random_User', 'no_brute_force_please' + 'x')
    assert b'Invalid username or password' in response.data


def test_new_unauthorized(client):
    client.cookie_jar.clear()
    response = client.get('/blog/new')
    assert response.status_code == 302


def test_new_authorized(client):
    login(client, 'Random_User', 'no_brute_force_please')
    response = client.get('/blog/new')
    assert response.status_code == 200


def test_new_successful(app, client):
    payload = dict(title='Testing Post', text='Example text')
    response = client.post('/blog/new', data=payload, follow_redirects=True)
    with app.app_context():
        added_post = Post.query.filter_by(title='Testing Post').first()
    assert added_post
