from django.db import models

class OTP(models.Model):
    mobile_number = models.CharField(max_length=10, unique=True)
    otp = models.CharField(max_length=6)
    attempts = models.PositiveIntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.mobile_number} - {self.otp} - {self.attempts}"
