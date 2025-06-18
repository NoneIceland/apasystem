from flask import Blueprint, render_template, flash, redirect, url_for
from app.forms.forms import RegistrationForm
from app.models import User
from app.extensions import db
from app.apis.verification import *
from app.services.verification import VerificationService
import re

register_bp = Blueprint('register', __name__)

@register_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    
    if form.validate_on_submit():
        email = form.email.data
        code = form.verification_code.data
        
        '''check if verification code valid'''
        is_valid, msg = VerificationService.verify_code(email, code)
        if not is_valid:
            flash(msg, 'danger')
            return render_template('auth/register.html', form=form)
        
        '''check if username unique'''
        if User.query.filter_by(username=form.username.data).first():
            form.username.errors.append('该用户名已被选择，请选择其他用户名')
            return render_template('auth/register.html', form=form)
        
        '''check if email unique'''
        if User.query.filter_by(email=form.email.data).first():
            form.email.errors.append('该邮箱已被注册，请使用其他邮箱')
            return render_template('auth/register.html', form=form)
        
        '''check if username valid'''
        
        '''create new user'''
        new_user = User(
            username=form.username.data,
            password=form.password.data,
            email=email,
            role='user'
        )
        
        db.session.add(new_user)
        db.session.commit()
        flash('注册成功！您现在可以登录', 'success')
        return redirect(url_for('login.login'))
    
    return render_template('auth/register.html', form=form)
        