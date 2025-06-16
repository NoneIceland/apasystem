from flask import Blueprint, request, jsonify, current_app
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app.services.verification import VerificationService
from app.utils.verification import send_verification_email

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=['5 per minute']
)

verification_bp = Blueprint('verification', __name__)

# @limiter.limit("3 per minute")
@verification_bp.route('/send-code', methods=['POST'])
def send_verification_code():
    # '''check if local'''
    # client_ip = request.remote_addr
    # internal_ip = current_app.config['INTERNAL_IP']
    # allowed_ips = [
    #     '127.0.0.1', 
    #     internal_ip
    # ]
    # if client_ip not in allowed_ips:
    #     return jsonify({
    #         "status": "error",
    #         "msg": "Forbidden: External access not allowed"
    #     }), 403
    
    '''send mails'''
    data = request.get_json()
    email = data.get('email')
    
    if not email:
        return jsonify({
            'status': 'error',
            'msg': '邮箱地址不能为空'
        }), 400
        
    code = VerificationService.generate_code()
    
    try:
        VerificationService.save_code(email, code)
        
        send_verification_email(email, code)
        
        return jsonify({
            'status': 'success',
            'msg': f'验证码已发送: {code}'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'msg': f'发送验证码失败: {e}'
        }), 500
        
@verification_bp.route('/verify-code', methods=['POST'])
def verify_code():
    data = request.get_json()
    email = data.get('email')
    code = data.get('code')
    
    if not email or not code:
        return jsonify({
            'status': 'error',
            'msg': '邮箱和验证码不能为空'
        }), 400
    
    is_valid, message = VerificationService.verify_code(email, code)
    
    if is_valid:
        VerificationService.delete_code(email)
        return jsonify({
            'status': 'success',
            'msg': message
        })
    else:
        return jsonify({
            'status': 'error',
            'msg': message
        }), 400