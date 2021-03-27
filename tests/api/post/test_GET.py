import pytest


@pytest.mark.parametrize('post_id', ['', '100'])
def test_GET_200_all_or_id(client, post_id):
    response = client.get('/api/post/' + post_id)
    assert response.status_code == 200


def test_GET_200_all_page(client):
    payload = dict(page=2)
    response = client.get('/api/post/', json=payload)
    assert response.status_code == 200


def test_GET_404_bad_id(client):
    response = client.get('/api/post/101')
    assert response.status_code == 404
