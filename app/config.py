import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    ''' basic config '''
    SECRET_KEY = os.getenv('SECRET_KEY', 'apasystem')
    WTF_CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    @staticmethod
    def init_app(app):
        ''' init recall '''
        pass
    
class DevelopmentConfig(Config):
    ''' development config '''
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}/{}'.format(
        os.getenv('DB_USER', 'root'),
        os.getenv('DB_PASSWORD', 'root'),
        os.getenv('DB_HOST', 'localhost'),
        os.getenv('DB_NAME', 'apa_system')
    )
    
class ProductionConfig(Config):
    ''' production config '''
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}/{}'.format(
        os.getenv('DB_USER', 'root'),
        os.getenv('DB_PASSWORD', 'root'),
        os.getenv('DB_HOST', 'localhost'),
        os.getenv('DB_NAME', 'apa_system')
    )
    
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
