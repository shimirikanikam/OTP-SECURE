from django.utils import timezone
import re, base64
from rest_framework.response import Response
import secrets
import string

def get_current_datetime():
    return timezone.now()

def mobile_number_pattern_validation(mobile_number):
        mobile_number_pattern = r'^[6-9]\d{9}$'
        if not re.match(mobile_number_pattern, mobile_number):
            return False
        else:
            return mobile_number_pattern

def otp_number_pattern_validation(user_otp):
    otp_pattern = r'^\d{6}$'
    if not re.match(otp_pattern, user_otp):
        return False
    else:
        return otp_pattern
    
def generate_otp(length=6):
    characters = string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

def mobile_number_decoder(mobile_number_base64):
    try:
        mobile_number = base64.b64decode(mobile_number_base64).decode('utf-8')
        return mobile_number
    except:
        return False