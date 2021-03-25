import pytest


def test_auth(app, client):
    payload = {
        'username': app.config['ADMIN_NAME'],
        'password': app.config['ADMIN_PASSWORD']
    }
    response = client.post('/api/auth/', json=payload)
    assert response.status_code == 200
