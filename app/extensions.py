from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from flask_redis import FlaskRedis

db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()
csrf = CSRFProtect()
migrate = Migrate()
redis_client = FlaskRedis()