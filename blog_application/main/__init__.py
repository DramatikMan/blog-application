import os
import json

from flask import Blueprint
from flask import redirect, url_for, render_template, flash, jsonify
from flask import current_app, session
from flask_login import login_user, logout_user, current_user
from flask_principal import Identity, AnonymousIdentity, identity_changed

from ..models import db, User
from ..extensions import oid, admin_permission
# from ..extensions import facebook
from ..forms import LoginForm, RegisterForm, OpenIDForm


bp_main = Blueprint(
    'main',
    __name__,
    template_folder=os.path.join('templates', 'main')
)


@bp_main.route('/')
def index():
    return redirect(url_for('blog.home'))


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
        user = User.query.filter_by(username=form.username.data).one()
        login_user(user, remember=form.remember.data)

        identity_changed.send(
            current_app._get_current_object(),
            identity=Identity(user.id)
        )

        kwargs = {}
        if 'ldf' in session:
            next_view = session['ldf']['name']
            kwargs = session['ldf']['kwargs']
            session.pop('ldf', None)
        else:
            next_view = 'home'

        flash('You have been logged in.', category='success')
        return redirect(url_for('blog.' + next_view, **kwargs))

    openid_errors = oid.fetch_error()
    if openid_errors:
        flash(openid_errors, category='danger')

    return render_template(
        'login.html',
        form=form,
        openid_form=openid_form
    )


@bp_main.route('/logout', methods=['GET', 'POST'])
def logout():
    if current_user.is_active:
        logout_user()

        identity_changed.send(
            current_app._get_current_object(),
            identity=AnonymousIdentity()
        )

        flash('You have been logged out.', category='success')

    return redirect(url_for('blog.home'))


@bp_main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        new_user = User(username=form.username.data)
        new_user.set_password(form.password.data)
        # new_user.roles = ['']
        db.session.add(new_user)
        db.session.commit()

        flash(
            'Your user has been created, please log in.',
            category='success'
        )

        return redirect(url_for('.login'))
    else:
        return render_template('register.html', form=form)


@bp_main.route('/current_user', methods=['GET'])
@admin_permission.require(http_exception=403)
def who_is_current_user():
    cu_dict = {}
    for item in dir(current_user):
        cu_dict[str(item)] = str(getattr(current_user, str(item)))
    return jsonify(cu_dict)


@bp_main.route('/flask_session', methods=['GET'])
@admin_permission.require(http_exception=403)
def flask_session_info():
    fs_dict = {}
    for item in dir(session):
        fs_dict[str(item)] = str(getattr(session, str(item)))
    return jsonify(fs_dict)


# @bp_main.route('/facebook')
# def facebook_login():
#     return facebook.authorize(
#         callback=url_for(
#             '.facebook_authorized',
#             next=request.referrer or None,
#             _external=True
#         )
#     )
#
#
# @bp_main.route('/facebook/authorized')
# def facebook_authorized(resp):
#     if resp is None:
#         reason = request.args['error_reason']
#         error = request.args['error_description']
#         return f'Access denied: reason={reason} error={error}'
#
#     session['facebook_oauth_token'] = (resp['access_token'], '')
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
#     flash('You have been logged in', category='success')
#
#     return redirect(
#         request.args.get('next') or url_for('blog_home')
#     )
