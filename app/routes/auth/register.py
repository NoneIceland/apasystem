from flask import Blueprint, render_template, redirect, url_for, flash
from app.forms.forms import RegistrationForm
from app.models import User
from app.extensions import db

register_bp = Blueprint('register', __name__)

@register_bp.route('/register', methods=['GET', 'POST'])
def register():
    registration_form = RegistrationForm()
    
    if registration_form.validate_on_submit():
        existing_user = User.query.filter_by(username=registration_form.username.data).first()
        if existing_user:
            flash('该用户名已被选择，请选择其他用户名', 'danger')
            return render_template('auth/register.html', form=registration_form)

        existing_nick = User.query.filter_by(nickname=registration_form.nickname.data).first()
        if existing_nick:
            flash('该昵称已被选择，请选择其他昵称', 'danger')
            return render_template('auth/register.html', form=registration_form)
        
        new_user = User(
            username=registration_form.username.data,
            nickname=registration_form.nickname.data,
            password=registration_form.password.data,
            role='user'
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('注册成功！您现在可以登录', 'success')
        return redirect(url_for('login.user_login'))
    
    return render_template('auth/register.html', form=registration_form)