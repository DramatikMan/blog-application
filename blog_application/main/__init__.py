import os
import json

from flask import Blueprint
from flask import redirect, url_for, render_template, flash, jsonify, abort
from flask import current_app, session, request
from flask_login import login_user, logout_user, current_user
from flask_principal import Identity, AnonymousIdentity, identity_changed

from ..models import db, User
from ..extensions import admin_permission
from ..forms import LoginForm, RegisterForm


bp_main = Blueprint(
    'main',
    __name__,
    static_folder='static',
    static_url_path='/main/static',
    template_folder='templates/main'
)


@bp_main.route('/')
def index():
    return redirect(url_for('blog.home'))


@bp_main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('blog.home'))

    if 'next_url' not in session:
        session['next_url'] = request.args.get('next')

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).one()
        login_user(user, remember=form.remember.data)

        identity_changed.send(
            current_app._get_current_object(),
            identity=Identity(user.id)
        )

        flash('You have been logged in.', category='success')
        next = session['next_url'] or url_for('blog.home')
        session.pop('next_url', None)
        return redirect(next)

    return render_template('login.html', form=form)


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
    if current_user.is_authenticated:
        return redirect(url_for('blog.home'))

    form = RegisterForm()

    if form.validate_on_submit():
        new_user = User(username=form.username.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()

        flash('Your user has been created, please log in.', category='success')
        return redirect(url_for('.login'))
    else:
        return render_template('register.html', form=form)
