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

@limiter.limit("3 per minute")
@verification_bp.route('/send-code', methods=['POST'])
def send_verification_code():
    data = request.get_json()
    
    if not data or 'email' not in data:
        return jsonify({
            'status': 'error',
            'message': 'arg:email not found'
        }), 400
        
    email = data['email']
    
    code = VerificationService.generate_code()
    try:
        VerificationService.save_code(email, code)
        send_verification_email(email, code)
        return jsonify({
            'status': 'success',
            'message': '验证码已发送，请查看您的邮箱!'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'验证码发送失败: {e}'
        }), 500


@limiter.limit("3 per minute")        
@verification_bp.route('/verify-code', methods=['POST'])
def verify_verification_code():
    data = request.get_json()
    
    if not data or 'email' not in data or 'code' not in data:
        return jsonify({
            'status': 'error',
            'message': 'args:email or code not found'
        }), 400
    
    email = data['email']
    code = data['code']
    
    is_valid, message = VerificationService.verify_code(email, code)
    
    return jsonify({
        'status': 'success' if is_valid else 'error',
        'is_valid': is_valid,
        'message': message
    })

@verification_bp.route('/find-code', methods=['POST'])
def find_verification_code():
    data = request.get_json()
    
    if not data or 'email' not in data:
        return jsonify({
            'status': 'error',
            'message': 'arg:email not found'
        })
    
    email = data['email']
    exists = VerificationService.get_code(email) is not None
    
    return jsonify({
        'status': 'success',
        'exists': exists,
        'message': 'verification code exists' if exists else 'verification code not exists'
    })