import pytest


@pytest.mark.parametrize('post_id', ['', '100'])
def test_posts_GET_200(client, post_id):
    response = client.get('/api/post/' + post_id)
    assert response.status_code == 200


def test_posts_GET_404(client):
    response = client.get('/api/post/101')
    assert response.status_code == 404


def test_posts_POST_405(client):
    response = client.post('/api/post/101')
    assert response.status_code == 405


def test_posts_POST_401(client):
    payload = {
        'title': 'Post 101',
        'text': 'Example text',
        'tags': 'pytest',
        'token': 'wrong'
    }
    response = client.post('/api/post/', json=payload)
    assert response.status_code == 401


def test_posts_POST_201(client):
    with client.session_transaction() as session:
        payload = {
            'title': 'Post 101',
            'text': 'Example text',
            'tags': 'pytest',
            'token': session['token']
        }
    response = client.post('/api/post/', json=payload)
    assert response.status_code == 201
