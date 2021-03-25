import pytest


def test_posts_get(client):
    response = client.get('/api/post/')
    assert response.status_code == 200
