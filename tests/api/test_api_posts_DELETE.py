def test_DELETE_405_no_id(client):
    response = client.delete('/api/post/')
    assert response.status_code == 405


def test_DELETE_404_bad_id(client):
    response = client.delete('/api/post/999')
    assert response.status_code == 404
