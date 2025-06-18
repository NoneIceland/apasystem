from flask import url_for
from app.extensions import db
from datetime import datetime

class UserInfo(db.Model):
    __tablename__ = 'user_info'
    
    id = db.Column(db.Integer, primary_key=True)
    
    '''link to TABLE users'''
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    
    '''info'''
    school_id = db.Column(db.String(10))
    gender = db.Column(db.Enum('male', 'female', 'other', name='gender_types'))
    birthday = db.Column(db.Date)
    phone = db.Column(db.String(20))
    bio = db.Column(db.Text)
    avatar = db.Column(db.String(255))
    
    user = db.relationship('User', back_populates='info', uselist=False)
    
    def __repr__(self):
        return f'<UserInfo {self.id} for User {self.user_id}>'
    
    def avatar_url(self):
        if self.avatar:
            clean_path = self.avatar.replace('\\', '/')
            return url_for('static', filename=f'uploads/{clean_path}', _external=True)
        return url_for('static', filename='images/default-avatar.png', _external=True)