from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class UserLoginForm(FlaskForm):
    username = StringField('用户名', validators=[
        DataRequired(message='用户名不能为空'), 
        Length(min=3, max=64, message='用户名应在3-64个字符之间')
    ])
    password = PasswordField('密码', validators=[
        DataRequired(message='密码不能为空'), 
        Length(min=6, max=64, message='用密码应在6-64个字符之间')
    ])
    remember_me = BooleanField('记住我')
    

class AdminLoginForm(FlaskForm):
    admin_id = StringField('管理员ID', validators=[
        DataRequired(), 
        Length(min=3, max=64)
    ])
    password = PasswordField('密码', validators=[
        DataRequired(), 
        Length(min=6, max=64)
    ])
    two_factor_code = StringField('两步验证码', validators=[
        DataRequired(), 
        Length(min=4, max=6)
    ])
    remember_me = BooleanField('记住我')

class VerificationForm(FlaskForm):
    email = StringField('邮箱', validators=[
        DataRequired(message='邮箱不能为空'),
        Email()
    ])
    submit = SubmitField('注册')

class RegistrationForm(FlaskForm):
    verification_code = StringField('验证码', validators=[
        DataRequired(message='验证码不能为空'),
        Length(min=6, max=6, message='验证码应为6位数字')
    ])
    username = StringField('用户名', validators=[
        DataRequired(message='用户名不能为空'),
        Length(min=3, max=64, message='用户名应在3-64个字符之间')
    ])
    email = StringField('邮箱', validators=[
        DataRequired(message='邮箱不能为空'),
        Email()
    ])
    password = PasswordField('密码', validators=[
        DataRequired(message='密码不能为空'),
        Length(min=6, max=64, message='用密码应在6-64个字符之间')
    ])
    confirm_password = PasswordField('确认密码', validators=[
        DataRequired(message='请确认密码'),
        EqualTo('password', message=' 两次输入的密码不一致')
    ])
    submit = SubmitField('注册')