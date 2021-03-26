import pytest

from blog_application.models import User


def test_auth(app, client):
    payload = {
        'username': app.config['ADMIN_NAME'],
        'password': app.config['ADMIN_PASSWORD']
    }
    response = client.post('/api/auth/', json=payload)
    json_data = response.get_json()
    with client.session_transaction() as session:
        session['token'] = json_data['token']
    with app.app_context():
        assert User.verify_auth_token(json_data['token']) == User.query.get(1)
