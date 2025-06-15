from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db

class Admin(UserMixin, db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(255))
    
    def __init__(self, admin_id, password):
        self.admin_id = admin_id
        self.set_password(password)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='scrypt')
        
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)