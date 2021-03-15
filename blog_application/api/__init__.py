import requests
import json

from flask import Blueprint, render_template, request, jsonify

from ..extensions import rest_api
from .post import PostApi
from .auth import AuthApi


rest_api.add_resource(
    PostApi,
    '/api/post',
    '/api/post/<int:post_id>',
    endpoint='api'
)
rest_api.add_resource(
    AuthApi,
    '/api/auth'
)


bp_api = Blueprint(
    'api',
    __name__,
    static_folder='static',
    template_folder='templates/api'
)


@bp_api.route('/', methods=['GET', 'POST'])
def index():
    return render_template('api.html')
