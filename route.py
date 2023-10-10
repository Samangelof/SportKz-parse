from flask import Blueprint, render_template
from markupsafe import escape


route_bp = Blueprint('route', __name__)

@route_bp.route('/')
def index():
    return render_template('index.html')


@route_bp.route('/hello')
def hello_world():
    return 'Hello world'


@route_bp.route('/users/<username>')
def show_user_profile(username):
    return f'User {escape(username)}'