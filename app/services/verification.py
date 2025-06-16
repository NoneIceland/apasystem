import random
import time
from datetime import timedelta
from app.extensions import redis_client

class VerificationService:
    @staticmethod
    def generate_code(length=6):
        '''generate numeric verification code'''
        return ''.join([str(random.randint(0, 9)) for _ in range(length)])
    
    @staticmethod
    def save_code(email, code, expire_minutes=5):
        '''save code in redis'''
        key = f"verification:code:{email}"
        
        redis_client.setex(
            name=key,
            time=timedelta(minutes=expire_minutes),
            value=code
        )
        
        redis_client.setex(
            name=f"verification:timestamp:{email}",
            time=timedelta(minutes=expire_minutes),
            value=int(time.time())
        )
        
        return True
    
    @staticmethod
    def get_code(email):
        '''get verification code'''
        key = f"verification:code:{email}"
        return redis_client.get(key)
    
    @staticmethod
    def verify_code(email, code):
        '''verify code'''
        stored_code = VerificationService.get_code(email)
        
        if not stored_code or stored_code.decode('utf-8') != code:
            return False, "验证码错误或已过期"
        
        timestamp_key = f"verification:timestamp:{email}"
        timestamp = redis_client.get(timestamp_key)
        if timestamp:
            create_time = int(timestamp.decode('utf-8'))
            if time.time() - create_time > 5 * 60:
                return False, "验证码已过期"
        
        return True, "验证成功"
    
    @staticmethod
    def delete_code(email):
        '''delete code'''
        keys = [
            f"verification:code:{email}",
            f"verification:timestamp:{email}"
        ]
        redis_client.delete(*keys)
        return True