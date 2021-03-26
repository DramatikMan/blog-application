import pytest


@pytest.mark.parametrize('post_id', ['', '100'])
def test_GET_200_all_or_id(client, post_id):
    response = client.get('/api/post/' + post_id)
    assert response.status_code == 200


def test_GET_404_bad_id(client):
    response = client.get('/api/post/101')
    assert response.status_code == 404


def test_POST_405_url_with_id(client):
    response = client.post('/api/post/101')
    assert response.status_code == 405


def test_POST_401_bad_token(client):
    payload = {
        'title': 'Post 101',
        'text': 'Example text',
        'tags': 'pytest',
        'token': 'wrong'
    }
    response = client.post('/api/post/', json=payload)
    assert response.status_code == 401


@pytest.mark.parametrize('tag_name', ['Python', 'pytest'])
def test_POST_201_created(client, tag_name):
    with client.session_transaction() as session:
        payload = {
            'title': 'Post 101',
            'text': 'Example text',
            'tags': tag_name,
            'token': session['token']
        }
    resp_json = client.post('/api/post/', json=payload).get_json()
    assert resp_json, response.status_code == [101, 201]


def test_PUT_405_no_id(client):
    response = client.put('/api/post/')
    assert response.status_code == 405


def test_PUT_404_bad_id(client):
    response = client.put('/api/post/999')
    assert response.status_code == 404


def test_PUT_401_bad_token(client):
    payload = {
        'title': 'Post 101',
        'text': 'Example text',
        'token': 'wrong'
    }
    response = client.put('/api/post/101', json=payload)
    assert response.status_code == 401


def test_PUT_403_wrong_user(client):
    with client.session_transaction() as session:
        payload = {
            'title': 'Post Edited',
            'text': 'Example text',
            'token': session['token']
        }
    response = client.put('/api/post/100', json=payload)
    assert response.status_code == 403


def test_PUT_201_edited(client):
    with client.session_transaction() as session:
        payload = {
            'title': 'Post Edited',
            'text': 'Example text',
            'tags': ['Python', 'Flask', 'Jinja', 'SQLAlchemy', 'сoverage'],
            'token': session['token']
        }
    resp_json = client.put('/api/post/1', json=payload).get_json()
    assert resp_json, response.status_code == [1, 201]


def test_DELETE_405_no_id(client):
    response = client.delete('/api/post/')
    assert response.status_code == 405


def test_DELETE_404_bad_id(client):
    response = client.delete('/api/post/999')
    assert response.status_code == 404
