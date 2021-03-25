import pytest


@pytest.mark.parametrize('post_id', ['', '100'])
def test_posts_get_200(client, post_id):
    response = client.get('/api/post/' + post_id)
    assert response.status_code == 200


def test_posts_get_404(client):
    response = client.get('/api/post/101')
    assert response.status_code == 404


def test_posts_post_405(client):
    response = client.post('/api/post/101')
    assert response.status_code == 405


# def test_posts_post(client):
#     payload = {
#         'title': 'Post 101',
#         'text': 'Example text',
#         'tags': 'pytest'
#     }
#     response = client.post('/api/post/', json=payload)
#     assert 101, response.status_code == [reponse.data['new_post.id'], 201]
