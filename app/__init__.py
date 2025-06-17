from flask import Flask
from flask_migrate import Migrate
from app.config import config
from app.const import bp_list
from sqlalchemy import text
from app.extensions import *


def create_app(config_name='default'):
    ''' Factory function to create the Flask app '''
    app = Flask(__name__)
    from app.extensions import db
    migrate = Migrate(app, db)
    
    '''load config'''
    app.config.from_object(config[config_name])
    
    '''init Flask_login'''
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))
    
    '''set login view'''
    login_manager.login_view = 'login.login'
    
    '''init flask config'''
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)
    redis_client.init_app(app)
    
    '''load mysql'''
    with app.app_context():
        db.create_all()

    '''register blueprints'''
    for bp_item in bp_list:
        blueprint = bp_item['bp']
        url_prefix = bp_item.get('url_prefix')
        
        app.register_blueprint(blueprint, url_prefix=url_prefix)
        
        
    '''mysql health check'''
    @app.route('/test/mysql')
    def test_mysql():
        try:
            db.session.execute(text('SELECT 1'))
            return 'OK'
        except Exception as e:
            return f'Error: {str(e)}'
    
    '''redis health check'''
    @app.route('/test/redis')
    def test_redis():
        try:
            return "OK"
        except Exception as e:
            return f"Error: {str(e)}"
    
    '''mail health check'''
    @app.route('/test/mail')
    def test_mail():
        from flask_mail import Message
        message = Message(subject='邮箱测试', recipients=["none3548393247@163.com"], body='这是一条测试邮件')
        mail.send(message)
        return 'mail test successfully!'
    
    return app