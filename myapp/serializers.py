from rest_framework import serializers

class VerifyOTPSerializer(serializers.Serializer):
    mobile_number_base64 = serializers.CharField(max_length=100)
    user_otp = serializers.CharField(max_length=6)

    