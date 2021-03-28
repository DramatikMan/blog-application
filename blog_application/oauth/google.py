from flask import flash
from flask_login import current_user, login_user
from flask_dance.contrib.google import make_google_blueprint
from flask_dance.consumer import oauth_authorized, oauth_error
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from sqlalchemy.orm.exc import NoResultFound
from ..models import db, User, OAuth


bp_google = make_google_blueprint(
    scope=[
        'https://www.googleapis.com/auth/userinfo.profile',
        'https://www.googleapis.com/auth/userinfo.email',
        'openid'
    ],
    storage=SQLAlchemyStorage(OAuth, db.session, user=current_user),
    redirect_to='blog.home'
)


@oauth_authorized.connect_via(bp_google)
def google_logged_in(blueprint, token):
    if not token:
        flash('Failed to log in.', category='danger')
        return False

    resp = blueprint.session.get('/oauth2/v1/userinfo')
    if not resp.ok:
        msg = 'Failed to fetch user info.'
        flash(msg, category='danger')
        return False

    info = resp.json()
    user_id = info['id']

    query = OAuth.query.filter_by(
        provider=blueprint.name,
        provider_user_id=user_id
    )
    try:
        oauth = query.one()
    except NoResultFound:
        oauth = OAuth(
            provider=blueprint.name,
            provider_user_id=user_id,
            token=token
        )

    if oauth.user:
        login_user(oauth.user)
        flash('Successfully signed in.', category='success')
    else:
        user = User(username=info['email'], email=info['email'])
        oauth.user = user
        db.session.add_all([user, oauth])
        db.session.commit()
        login_user(user)

    flash('Successfully signed in.', category='success')
    return False


@oauth_error.connect_via(bp_google)
def google_error(blueprint, message, response):
    msg = (
        f'OAuth error from {blueprint.name}! '
        f'message={message} response={response}'
    )
    flash(msg, category="danger")
