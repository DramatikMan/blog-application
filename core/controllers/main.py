import flask

from core.forms import LoginForm, RegisterForm
from core.models import db, User


bp_main = flask.Blueprint(
    'main',
    __name__,
    template_folder='../templates/main'
)


@bp_main.route('/')
def index():
    return flask.redirect(flask.url_for('blog.home'))


@bp_main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        flask.flash('You have been logged in.', category='success')
        return flask.redirect(flask.url_for('blog.home'))

    return flask.render_template('login.html', form=form)


@bp_main.route('/logout', methods=['GET', 'POST'])
def logout():
    flask.flash('You have been logged out', category='success')
    return flask.redirect(flask.url_for('.home'))


@bp_main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        new_user = User()
        new_user.username = form.username.sidebar_data
        new_user.set_password(form.username_data)
        db.session.add(new_user)
        db.session.commit()

        flask.flash(
            'Your user has been created, please log in.',
            category='success'
        )

        return flask.redirect(flask.url_for('.login'))

    return flask.render_template('register.html', form=form)
