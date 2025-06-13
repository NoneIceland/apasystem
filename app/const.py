from app.routes.main import main_bp
from app.routes.auth.user import user_bp
from app.routes.auth.admin import admin_bp
from app.routes.auth.login import login_bp
from app.routes.auth.logout import logout_bp

'''register blueprint here'''
bp_list = [
    {'bp':main_bp, 'url_prefix': '/'},
    {'bp':login_bp, 'url_prefix': '/'},
    {'bp':logout_bp, 'url_prefix': '/'},
    {'bp':user_bp, 'url_prefix': '/'},
    {'bp':admin_bp, 'url_prefix': '/'}
]
