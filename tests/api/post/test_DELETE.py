def test_DELETE_405_no_id(client):
    response = client.delete('/api/post/')
    assert response.status_code == 405


def test_DELETE_404_bad_id(client):
    response = client.delete('/api/post/999')
    assert response.status_code == 404


def test_DELETE_400_bad_payload(client):
    payload = {'bad_payload': 'value'}
    response = client.delete('/api/post/1')
    assert response.status_code == 400


def test_DELETE_401_bad_token(client):
    payload = {'token': 'wrong'}
    response = client.delete('/api/post/1', json=payload)
    assert response.status_code == 401


def test_DELETE_403_wrong_user(client):
    with client.session_transaction() as session:
        payload = {'token': session['token']}
    response = client.delete('/api/post/100', json=payload)
    assert response.status_code == 403


def test_DELETE_204_deleted(client):
    with client.session_transaction() as session:
        payload = {'token': session['token']}
    response = client.delete('/api/post/1', json=payload)
    assert response.status_code == 204
