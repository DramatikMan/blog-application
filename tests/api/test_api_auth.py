from blog_app.models import User


def test_getting_valid_token(app, client):
    payload = dict(
        username=app.config['ADMIN_NAME'],
        password=app.config['ADMIN_PASSWORD']
    )
    response = client.post('/api/auth/', json=payload)
    json_data = response.get_json()
    with client.session_transaction() as session:
        session['token'] = json_data['token']
    with app.app_context():
        admin = User.query.get(1)
        user_from_token = User.verify_auth_token(json_data['token'])
    assert admin == user_from_token


def test_401_wrong_password(client):
    payload = dict(username='Random_User', password='wrong_password')
    response = client.post('/api/auth/', json=payload)
    assert response.status_code == 401
