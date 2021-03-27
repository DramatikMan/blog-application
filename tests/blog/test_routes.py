from blog_application.forms import CommentForm
from blog_application.models import Comment


def test_home(client):
    response = client.get('/blog')
    assert b'Recent Posts' in response.data
    assert b'Popular Tags' in response.data


def test_post_page(client):
    response = client.get('/blog/post/100')
    assert b'Written by' in response.data
    assert b'New comment' in response.data


def test_add_comment(app, client):
    url = '/blog/post/100'
    with app.test_request_context(url):
        form = CommentForm()
        form.name.data = 'tester'
        form.text.data = 'Example comment'
        client.post(url, data=form.data)
    with app.app_context():
        added_comment = Comment.query.filter_by(text='Example comment').first()
    assert added_comment
