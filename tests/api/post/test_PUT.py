def test_PUT_405_no_id(client):
    response = client.put('/api/post/')
    assert response.status_code == 405


def test_PUT_404_bad_id(client):
    response = client.put('/api/post/999')
    assert response.status_code == 404


def test_PUT_400_bad_payload(client):
    payload = dict(bad_payload='value')
    response = client.put('/api/post/100', json=payload)
    assert response.status_code == 400


def test_PUT_401_bad_token(client):
    payload = dict(
        title='Post 101',
        text='Example text',
        token='wrong'
    )
    response = client.put('/api/post/101', json=payload)
    assert response.status_code == 401


def test_PUT_403_wrong_user(client):
    with client.session_transaction() as session:
        payload = dict(
            title='Post Edited',
            text='Example text',
            token=session['token']
        )
    response = client.put('/api/post/100', json=payload)
    assert response.status_code == 403


def test_PUT_201_edited(client):
    with client.session_transaction() as session:
        payload = dict(
            title='Post Edited',
            text='Example text',
            tags=['Python', 'Flask', 'Jinja', 'SQLAlchemy', 'сoverage'],
            token=session['token']
        )
    resp_json = client.put('/api/post/2', json=payload).get_json()
    assert resp_json, response.status_code == [1, 201]
