import pytest


def test_POST_405_url_with_id(client):
    response = client.post('/api/post/101')
    assert response.status_code == 405


def test_POST_400_bad_payload(client):
    payload = {'bad_payload': 'value'}
    response = client.post('/api/post/', json=payload)
    assert response.status_code == 400


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
