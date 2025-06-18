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
    WTF_CSRF_ENABLED = False
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}/{}'.format(
        os.getenv('DB_USER', 'root'),
        os.getenv('DB_PASSWORD', 'root'),
        os.getenv('DB_HOST', 'localhost'),
        os.getenv('DB_NAME', 'apa_system')
    )
    
    REDIS_HOST = "localhost"
    REDIS_PORT = 6379
    REDIS_PASSWORD = None
    REDIS_DB = 0
    REDIS_URL = 'redis://localhost:6379/0'
    
    MAIL_SERVER = "smtp.163.com"
    MAIL_USE_SSL = True
    MAIL_PORT = 465
    MAIL_USERNAME = "icemail2025@163.com"
    MAIL_PASSWORD = "LUeRm648ntRVmQ6g"
    MAIL_DEFAULT_SENDER = "icemail2025@163.com"
    INTERNAL_IP = "localhost"
    
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
    AVATAR_FOLDER = 'avatars'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024
    
class ProductionConfig(Config):
    ''' production config '''
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}/{}'.format(
        os.getenv('DB_USER', 'root'),
        os.getenv('DB_PASSWORD', 'root'),
        os.getenv('DB_HOST', 'localhost'),
        os.getenv('DB_NAME', 'apa_system')
    )
    REDIS_URL = 'redis://localhost:6379/0'
    REDIS_HOST = "localhost"
    REDIS_PASSWORD = None
    REDIS_PORT = 6379
    REDIS_DB = 0
    
    
    MAIL_SERVER = "smtp.163.com"
    MAIL_USE_SSL = True
    MAIL_PORT = 465
    MAIL_USERNAME = "icemail2025@163.com"
    MAIL_PASSWORD = "LUeRm648ntRVmQ6g"
    MAIL_DEFAULT_SENDER = "icemail2025@163.com"
    INTERNAL_IP = ""
    
    
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
