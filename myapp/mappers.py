from .models import OTP
from .utils import get_current_datetime
from .constants import OTP_EXPIRY_MINUTES
from datetime import timedelta


class OTPMapper:
    def __init__(self, mobile_number):
        self.mobile_number = mobile_number

    def get_active_otp(self):
        return OTP.objects.filter(
            mobile_number=self.mobile_number,
            timestamp__gte=get_current_datetime() - timedelta(minutes=OTP_EXPIRY_MINUTES)
        ).first()

    def create_otp(self, otp, attempts):
        return OTP.objects.create(
            mobile_number=self.mobile_number,
            otp=otp,
            attempts=attempts
        )

    def update_otp(self, otp_obj, otp, attempts):
        otp_obj.otp = otp
        otp_obj.attempts = attempts
        otp_obj.save()

    def delete_expired_otps(self):
        timestamp_limit = get_current_datetime() - timedelta(minutes=OTP_EXPIRY_MINUTES)
        return OTP.objects.filter(
            mobile_number=self.mobile_number,
            timestamp__lt=timestamp_limit
        ).delete()
