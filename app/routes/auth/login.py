from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, current_user, logout_user
from ...forms.forms import UserLoginForm, AdminLoginForm
from ...models import User, Admin

login_bp = Blueprint('login', __name__)

@login_bp.route('/user_login', methods=['GET', 'POST'])
def user_login():
    '''if Login, redirect to main'''
    if current_user.is_authenticated:
        return redirect(url_for('main.main'))
    
    form = UserLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user and user.verify_password(form.password.data):
            login_user(user)
            flash('用户登录成功!', 'success')
            return redirect(url_for('main.main'))
        else:
            flash('用户名或密码错误!', 'danger')
            
    return render_template('auth/user_login.html', form=form)



@login_bp.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    '''if admin login, redirect to admin'''
    if current_user.is_authenticated and isinstance(current_user, Admin):
        return redirect(url_for('main.main'))
    
    form = AdminLoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(admin_id=form.admin_id.data).first()
        
        if admin and admin.verify_password(form.password.data):
            login_user(admin)
            flash('管理员登录成功！', 'success')
            return redirect(url_for('main.main'))
        else:
            flash('管理员ID或密码错误!', 'danger')

    return render_template('auth/admin_login.html', form=form)

@login_bp.route('/logout')
def logout():
    logout_user()
    flash('您已退出登录！', 'info')
    return redirect(url_for('login.user_login'))