def login(client, username, password):
    payload = dict(username=username, password=password)
    return client.post('/login', data=payload, follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)
