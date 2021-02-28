import flask

from core.models import db, User
from core.extensions import oid
# from core.extensions import facebook
from core.forms import LoginForm, RegisterForm, OpenIDForm


bp_main = flask.Blueprint(
    'main',
    __name__,
    template_folder='../templates/main'
)


@bp_main.route('/')
def index():
    return flask.redirect(flask.url_for('blog.home'))


# @bp_main.route('/facebook')
# def facebook_login():
#     return facebook.authorize(
#         callback=flask.url_for(
#             '.facebook_authorized',
#             next=flask.request.referrer or None,
#             _external=True
#         )
#     )
#
#
# @bp_main.route('/facebook/authorized')
# def facebook_authorized(resp):
#     if resp is None:
#         reason = flask.request.args['error_reason']
#         error = flask.request.args['error_description']
#         return f'Access denied: reason={reason} error={error}'
#
#     flask.session['facebook_oauth_token'] = (resp['access_token'], '')
#
#     me = facebook.get('/me')
#     fname = me.data['first_name']
#     lname = me.data['last_name']
#     user = User.query.filter_by(username=fname + ' ' + lname).first()
#     if not user:
#         user = User(fname + ' ' + lname)
#         db.session.add(user)
#         db.session.commt()
#
#     flask.flash('You have been logged in', category='success')
#
#     return flask.redirect(
#         flask.request.args.get('next') or flask.url_for('blog_home')
#     )


@bp_main.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    form = LoginForm()
    openid_form = OpenIDForm()

    if openid_form.validate_on_submit():
        return oid.try_login(
            openid_form.openid.data,
            ask_for=['nickname', 'email'],
            ask_for_optional=['fullname']
        )

    if form.validate_on_submit():
        flask.flash('You have been logged in.', category='success')
        return flask.redirect(flask.url_for('blog.home'))

    openid_errors = oid.fetch_error()
    if openid_errors:
        flask.flash(openid_errors, category='danger')

    return flask.render_template(
        'login.html',
        form=form,
        openid_form=openid_form
    )


@bp_main.route('/logout', methods=['GET', 'POST'])
def logout():
    flask.flash('You have been logged out.', category='success')
    return flask.redirect(flask.url_for('.home'))


@bp_main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        new_user = User(username=form.username.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()

        flask.flash(
            'Your user has been created, please log in.',
            category='success'
        )

        return flask.redirect(flask.url_for('.login'))
    else:
        return flask.render_template('register.html', form=form)
