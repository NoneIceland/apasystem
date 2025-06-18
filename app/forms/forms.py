from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DateField, TextAreaField, FileField
from wtforms.validators import DataRequired, Length, EqualTo, Email, Optional, ValidationError
from app.utils.validator import alphanumeric_only
from app.models.User import User
from app.models.UserInfo import UserInfo
from flask_login import current_user

class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[
        DataRequired(message='用户名不能为空'), 
        Length(min=3, max=64, message='用户名应在3-64个字符之间'),
        alphanumeric_only
    ])
    password = PasswordField('密码', validators=[
        DataRequired(message='密码不能为空'), 
        Length(min=6, max=64, message='用密码应在6-64个字符之间')
    ])
    remember_me = BooleanField('记住我')

class RegistrationForm(FlaskForm):
    verification_code = StringField('验证码', validators=[
        DataRequired(message='验证码不能为空'),
        Length(min=6, max=6, message='验证码应为6位数字')
    ])
    username = StringField('用户名', validators=[
        DataRequired(message='用户名不能为空'),
        Length(min=3, max=64, message='用户名应在3-64个字符之间'),
        alphanumeric_only
    ])
    nickname = StringField('昵称', validators=[
        DataRequired(message='昵称不能为空'),
        Length(min=1, max=16, message='昵称应在1-16个字符之间')
    ])
    email = StringField('邮箱', validators=[
        DataRequired(message='邮箱不能为空'),
        Email()
    ])
    password = PasswordField('密码', validators=[
        DataRequired(message='密码不能为空'),
        Length(min=6, max=64, message='密码应在6-64个字符之间')
    ])
    confirm_password = PasswordField('确认密码', validators=[
        DataRequired(message='请确认密码'),
        EqualTo('password', message=' 两次输入的密码不一致')
    ])
    submit = SubmitField('注册')
    
class ProfileForm(FlaskForm):
    username = StringField('用户名', render_kw={'readonly': True})
    nickname = StringField('昵称', validators=[
        DataRequired(message='昵称不能为空'),
        Length(min=1, max=16, message='昵称应在1-16个字符之间')
    ])
    email = StringField('邮箱', render_kw={'readonly': True})
    phone = StringField('手机号码', validators=[
        Optional(),
        Length(min=11, max=11, message='手机号码必须是11位数字')
    ])
    school_id = StringField('学号/工作号', validators=[
        Optional(),
        Length(min=10, max=10, message='学号/工作号必须是10位数字')
    ])
    gender = SelectField('性别', choices=[
        ('', '请选择'),
        ('male', '男'),
        ('female', '女'),
        ('other', '其他')
    ], validators=[Optional()])
    birthday = DateField('生日', format='%Y-%m-%d', validators=[Optional()])
    bio = TextAreaField('个人简介', validators=[
        Optional(),
        Length(max=500, message='个人简介不能超过500个字')
    ])
    avatar = FileField('头像', validators=[
        FileAllowed(['jpg', 'png', 'jpeg', 'gid'], '只允许上传图片文件')
    ])
    submit = SubmitField('保存更改')
    
    def validate_nickname(self, field):
        if field.data != current_user.nickname:
            user = User.query.filter_by(nickname=field.data).first()
            if user:
                raise ValidationError('该昵称已被其他用户使用')
            
    def validate_phone(self, field):
        if field.data:
            if not field.data.isdigit():
                raise ValidationError('手机号必须由数字组成')
            
            user_info = UserInfo.query.filter_by(phone=field.data).first()
            if user_info and user_info.user_id != current_user.id:
                raise ValidationError('该手机号已被其他用户使用')
    
    def populate_from_user(self, user):
        self.username.data = user.username
        self.nickname.data = user.nickname
        self.email.data = user.email
        
        if user.info:
            self.phone.data = user.info.phone
            self.school_id.data = user.info.school_id
            self.gender.data = user.info.gender
            self.birthday.data = user.info.birthday
            self.bio.data = user.info.bio