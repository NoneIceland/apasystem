from app.routes.main import main_bp

from app.routes.auth.login import login_bp
from app.routes.auth.register import register_bp

from app.routes.home.home import home_bp

'''register blueprint here'''
bp_list = [
    {'bp':main_bp, 'url_prefix': '/'},
    {'bp':login_bp, 'url_prefix': '/auth'},
    {'bp':register_bp, 'url_prefix': '/auth'},
    {'bp':home_bp, 'url_prefix': '/'}
]
