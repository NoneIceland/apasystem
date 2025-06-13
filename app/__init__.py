from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import config
from app.const import bp_list
from sqlalchemy import text

db = SQLAlchemy()

def create_app(config_name='default'):
    ''' Factory function to create the Flask app '''
    app = Flask(__name__)
    
    '''load config'''
    app.config.from_object(config[config_name])
    
    '''load mysql'''
    db.init_app(app)

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