from datetime import timedelta
from .constants import MAX_OTP_ATTEMPTS, OTP_EXPIRY_MINUTES
import secrets
import string
from .mappers import OTPMapper
from .utils import get_current_datetime
from .utils import generate_otp


class OTPService:
    @staticmethod
    def request_otp(mobile_number):
        current_datetime = get_current_datetime()
        otp_mapper = OTPMapper(mobile_number)

        otp_obj = otp_mapper.get_active_otp()

        if otp_obj and otp_obj.attempts >= MAX_OTP_ATTEMPTS:
            return None, f'Maximum attempts reached. Try again after {OTP_EXPIRY_MINUTES} mins.'

        create_new = not otp_obj or current_datetime >= otp_obj.timestamp + timedelta(minutes=OTP_EXPIRY_MINUTES)

        if create_new:
            otp_mapper.delete_expired_otps()
            otp_obj = otp_mapper.create_otp(generate_otp(), 1)
            return otp_obj.otp, 'OTP sent successfully.'

        otp_mapper.update_otp(otp_obj, generate_otp(), otp_obj.attempts + 1)
        otp_obj.timestamp = current_datetime
        otp_obj.save()
        return otp_obj.otp, 'OTP resent successfully.'

    @staticmethod
    def verify_otp(mobile_number, user_otp):
        
        otp_mapper = OTPMapper(mobile_number)
        
        otp_obj = otp_mapper.get_active_otp()

        if not otp_obj:
            return False, 'OTP not found. Please request OTP first.'

        if otp_obj.attempts >= MAX_OTP_ATTEMPTS:
            return False, f'Maximum attempts reached. Try again after {OTP_EXPIRY_MINUTES} mins.'

        if otp_obj.otp == user_otp:
            otp_obj.delete()
            return True, 'OTP verified successfully.'

        return False, 'Incorrect OTP. Please try again.'