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


def test_new_post_unauthorized(client):
    response = client.get('/blog/new', follow_redirects=True)
    assert response.status_code == 302
    assert b'Please log in to access this page.' in response.data


def test_new_post(client):
    login(client, 'Random_User', 'no_brute_force_please')
    response = client.get('/blog/new', follow_redirects=True)
    assert response.status_code == 200
    assert b'Content' in response.data
