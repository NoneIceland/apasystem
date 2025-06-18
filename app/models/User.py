from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from app.models.UserInfo import UserInfo

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    nickname = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(128), unique=True)
    password_hash = db.Column(db.String(255))
    role = db.Column(db.String(32), default='user')
    is_verified = db.Column(db.Boolean, default=False)
    
    '''be link to TABLE user_info'''
    info = db.relationship('UserInfo', back_populates='user', uselist=False, cascade='all, delete-orphan')
    
    def __init__(self, username, nickname, email, password, role='user'):
        self.username = username
        self.nickname = nickname
        self.email = email
        self.set_password(password)
        self.role = role
        
    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='scrypt')
        
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def create_info(self):
        if not self.info:
            self.info = UserInfo(user_id=self.id)
        return self.info