from flask import Blueprint, render_template, flash, redirect, url_for, current_app
from flask_login import current_user, login_required
from app.forms.forms import ProfileForm
from app.extensions import db
from werkzeug.utils import secure_filename
from pathlib import Path
import os
import uuid

userinfo_bp = Blueprint('userinfo', __name__)

@userinfo_bp.route('/edit', methods=['GET', 'POST'])
@login_required
def userinfo_edit():
    form = ProfileForm()
    
    if not form.is_submitted():
        form.populate_from_user(current_user)
    
    if form.validate_on_submit():
        try:
            current_user.nickname = form.nickname.data

            current_user.info.phone = form.phone.data or None
            current_user.info.school_id = form.school_id.data or None
            current_user.info.gender = form.gender.data or None
            current_user.info.birthday = form.birthday.data
            current_user.info.bio = form.bio.data
            
            '''delete old avatar jpg'''
            if current_user.info.avatar:
                upload_dir = Path(current_app.config['UPLOAD_FOLDER'])
                old_avatar_path = upload_dir / current_user.info.avatar
            
            '''uploads avatar jpg'''
            if form.avatar.data:
                upload_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], current_app.config['AVATAR_FOLDER'])
                os.makedirs(upload_dir, exist_ok=True)
                
                original_filename = secure_filename(form.avatar.data.filename)
                _, file_extension = os.path.splitext(original_filename)
                
                filename = f"{uuid.uuid4().hex}{file_extension}"
                
                avatar_path = os.path.join(upload_dir, filename)
                form.avatar.data.save(avatar_path)
                
                current_user.info.avatar = os.path.join('avatars', filename)
            
            db.session.commit()
            
            if old_avatar_path and old_avatar_path.exists():
                try:
                    old_avatar_path.unlink()
                except Exception as e:
                    current_app.logger.error(f"删除旧头像失败: {str(e)}")
            
            flash('个人信息更新成功！', 'success')
            return redirect(url_for('userinfo.userinfo_edit'))
        
        except Exception as e:
            db.session.rollback()
            flash(f'更新失败: {str(e)}', 'danger')
        
    
    return render_template('user/userinfo_edit.html', form=form)