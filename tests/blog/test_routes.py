def test_home(client):
    response = client.get('/blog')
    assert b'Recent Posts' in response.data
    assert b'Popular Tags' in response.data
