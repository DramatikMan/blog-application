from blog_app.models import User, Post, Comment, Tag, Role

def test_repr(app):
    with app.app_context():
        user = User.query.filter_by(username='Random_User').one()
        post = Post.query.filter_by(id=33).one()
        comment = Comment.query.filter_by(text='Example comment').first()
        tag = Tag.query.filter_by(title='Flask').one()
        role = Role.query.filter_by(name='poster').one()
    assert str(user) == f"<User '{user.username}'>"
    assert str(post) == f"<Post '{post.title}'>"
    assert str(comment) == f"<Comment '{comment.text[:15]}'>"
    assert str(tag) == f"<Tag '{tag.title}'>"
    assert str(role) == f"<Role '{role.name}'>"
