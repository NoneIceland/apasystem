from flask import Blueprint

logout_bp = Blueprint('logout', __name__)

@logout_bp.route('/logout')
def logout():
    return 'logout page'
