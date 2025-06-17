from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, current_user, logout_user
from ...forms.forms import LoginForm
from ...models import User

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    '''if user login, redirect to home'''
    if current_user.is_authenticated and isinstance(current_user, User):
        return redirect(url_for('home.home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user and user.verify_password(form.password.data):
            login_user(user)
            flash('用户登录成功!', 'success')
            return redirect(url_for('home.home'))
        else:
            flash('用户名或密码错误!', 'danger')
            
    return render_template('auth/login.html', form=form)

@login_bp.route('/logout')
def logout():
    logout_user()
    flash('您已退出登录！', 'info')
    return redirect(url_for('login.login'))