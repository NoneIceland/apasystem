from flask import current_app
from flask_mail import Message
import threading

def send_verification_email(email, code):
    """send verification email"""
    msg = Message(
        subject='您的邮箱验证码',
        recipients=[email],
        sender=current_app.config['MAIL_DEFAULT_SENDER']
    )
    msg.body = f'您的验证码是：{code}\n\n'
    msg.body += '此验证码用于账号注册，有效期为5分钟。\n'
    msg.body += '请勿将此验证码告诉他人。\n'
    
    app = current_app._get_current_object()
    
    thread = threading.Thread(
        target=send_async_email,
        args=(app, msg)
    )
    thread.start()
    

def send_async_email(app, msg):
    """async sending email"""
    with app.app_context():
        from app import mail
        try:
            mail.send(msg)
        except Exception as e:
            app.logger.error(f'邮件发送失败：{str(e)}')