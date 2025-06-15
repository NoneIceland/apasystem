from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(255))
    role = db.Column(db.String(32), default='user')
    
    def __init__(self, username, password, role='user'):
        self.username = username
        self.set_password(password)
        self.role = role
        
    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='scrypt')
        
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @staticmethod
    def create_user(username, password):
        '''create user helper'''
        if User.query.filter_by(username=username).first():
            return None
        
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return new_user