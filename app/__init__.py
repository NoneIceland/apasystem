from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from app.config import config
from app.const import bp_list
from sqlalchemy import text
from app.extensions import db

user_login_manager = LoginManager()
admin_login_manager = LoginManager()

def create_app(config_name='default'):
    ''' Factory function to create the Flask app '''
    app = Flask(__name__)    
    
    '''load config'''
    app.config.from_object(config[config_name])
    
    '''init Flask-Login'''
    
    @user_login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        user = User.query.get(int(user_id))
        if user:
            return user
        return None
    
    @admin_login_manager.user_loader
    def load_admin(admin_id):
        from app.models import Admin
        admin = Admin.query.get(int(admin_id))
        if admin:
            return admin
        return None
    
    user_login_manager.init_app(app)
    admin_login_manager.init_app(app)
    
    '''init CSRFProtect'''
    csrf = CSRFProtect()
    csrf.init_app(app)
    
    '''load mysql'''
    db.init_app(app)
    with app.app_context():
        db.create_all()

    '''register blueprints'''
    for bp_item in bp_list:
        blueprint = bp_item['bp']
        url_prefix = bp_item.get('url_prefix')
        
        app.register_blueprint(blueprint, url_prefix=url_prefix)
        
        
    '''mysql health check'''
    @app.route('/healthcheck')
    def db_healthcheck():
        try:
            db.session.execute(text('SELECT 1'))
            return 'OK'
        except Exception as e:
            return f'Error: {str(e)}'
    
    return app