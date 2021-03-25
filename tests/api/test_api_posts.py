import pytest


@pytest.mark.parametrize('post_id', ['', '100'])
def test_posts_get_200(client, post_id):
    response = client.get('/api/post/' + post_id)
    assert response.status_code == 200


def test_posts_get_404(client):
    response = client.get('/api/post/101')
    assert response.status_code == 404
