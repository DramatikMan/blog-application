from sqlalchemy import text

from blog_application.models import db, Post, User
from blog_application.forms import RegisterForm
from .utils import login, logout


def test_login_logout(client):
    response = client.post('/login', data={})
    assert b'Enter your login credentials:' in response.data

    response = login(client, 'Random_User', 'no_brute_force_please')
    assert b'You have been logged in.' in response.data

    response = client.get('/login')
    assert response.status_code == 302

    response = client.get('/register')
    assert response.status_code == 302

    response = logout(client)
    assert b'You have been logged out.' in response.data

    response = login(client, 'Random_User' + 'x', 'no_brute_force_please')
    assert b'Invalid username or password' in response.data

    response = login(client, 'Random_User', 'no_brute_force_please' + 'x')
    assert b'Invalid username or password' in response.data


def test_sign_up_page(client):
    response = client.get('/register')
    assert response.status_code == 200


def test_sign_up_already_exists(client):
    payload = dict(
        username='Random_User',
        password='_8_chars',
        confirm='_8_chars'
    )
    response = client.post('/register', data=payload, follow_redirects=True)
    assert b'User with that name already exists.' in response.data


def test_sign_up_short_pswd(client):
    payload = dict(
        username='tester',
        password='short',
        confirm='short'
    )
    response = client.post('/register', data=payload, follow_redirects=True)
    assert b'Field must be at least 8 characters long.' in response.data


def test_sign_up_success(app, client):
    payload = dict(
        username='tester',
        password='_8_chars',
        confirm='_8_chars'
    )
    response = client.post('/register', data=payload, follow_redirects=True)
    with app.app_context():
        registered = User.query.filter_by(username='tester').one()
    assert registered
    assert b'Enter your login credentials:' in response.data


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


def test_edit_unauthorized(client):
    response = client.get('/blog/edit/25')
    assert response.status_code == 403


def test_edit_authorized(client):
    response = client.get('/blog/edit/100')
    assert response.status_code == 200


def test_edit_successful(app, client):
    payload = dict(title='Post Edited', text='Example text')
    response = client.post('/blog/edit/100', data=payload, follow_redirects=True)
    with app.app_context():
        edited_post = Post.query.filter_by(id=100).first()
    assert edited_post.title == 'Post Edited'


def test_edit_no_role(app, client):
    with app.app_context():
        random_user = User.query.filter_by(username='Random_User').one()
        s = text(f'''
            DELETE FROM test.user_x_role
            WHERE
                user_id = {random_user.id}
            AND role_id = 2
        ''')
        db.engine.execute(s)
    response = client.post('/blog/edit/100')
    assert response.status_code == 403
