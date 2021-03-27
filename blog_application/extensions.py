import datetime

from flask import flash, redirect, url_for, session, current_app, request
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
from flask_principal import Principal, Permission, RoleNeed
from flask_restful import Api


migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
principals = Principal()
rest_api = Api()

login_manager.login_view = 'main.login'
login_manager.session_protection = 'strong'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

admin_permission = Permission(RoleNeed('admin'))
poster_permission = Permission(RoleNeed('poster'))
default_permission = Permission(RoleNeed('default'))


def datetimeformat(value, format='%d-%m-%Y %H:%M'):
    return value.strftime(format)
