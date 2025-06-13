from flask import Blueprint

login_bp = Blueprint('login', __name__)

@login_bp.route('/login')
def login():
    return 'login page'
