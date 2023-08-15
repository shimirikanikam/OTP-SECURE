from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services import OTPService
import base64
from .serializers import VerifyOTPSerializer
from .utils import mobile_number_pattern_validation, otp_number_pattern_validation,mobile_number_decoder,get_client_ip
from django.core.cache import cache
from rest_framework import status

@api_view(['POST'])
def request_otp_view(request):
    mobile_number_base64 = request.data.get('mobile_number')
    mobile_number= mobile_number_decoder(mobile_number_base64)
    if not mobile_number:
        return Response({'error': 'Invalid base64 encoding or decoding error.'}, status=status.HTTP_400_BAD_REQUEST)
    if not mobile_number_pattern_validation(mobile_number):
        return Response({'error': 'Please provide a valid 10-digit mobile number starting with a digit between 6 and 9.'}, status=status.HTTP_400_BAD_REQUEST)
    mobile_number_pattern_validation(mobile_number)
    ip_address = get_client_ip(request)
    requested_numbers = cache.get(ip_address, [])
    otp, message = OTPService.request_otp(mobile_number)
    if not otp:
        return Response({'error': message}, status=status.HTTP_429_TOO_MANY_REQUESTS)
    if len(requested_numbers) >= 5:
        return Response({'error': 'Maximum number request reached for this IP.'}, status=status.HTTP_429_TOO_MANY_REQUESTS)
    requested_numbers.append(mobile_number)
    cache.set(ip_address, requested_numbers, 3600)
    return Response({'otp': otp, 'message': message}, status=status.HTTP_200_OK)

@api_view(['POST'])
def verify_otp_view(request):
    serializer = VerifyOTPSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    mobile_number_base64 = serializer.validated_data['mobile_number_base64']
    user_otp = serializer.validated_data['user_otp']

    mobile_number= mobile_number_decoder(mobile_number_base64)
    if not mobile_number:
        return Response({'error': 'Invalid base64 encoding or decoding error.'}, status=status.HTTP_400_BAD_REQUEST)
    if not mobile_number_pattern_validation(mobile_number):
        return Response({'error': 'Please provide a valid 10-digit mobile number starting with a digit between 6 and 9.'}, status=status.HTTP_400_BAD_REQUEST)
    mobile_number_pattern_validation(mobile_number)

    if not otp_number_pattern_validation(user_otp):
        return Response({'error': 'Please provide a valid 6-digit OTP.'}, status=status.HTTP_400_BAD_REQUEST)
    otp_number_pattern_validation(user_otp)

    is_verified, message = OTPService.verify_otp(mobile_number, user_otp)
    if is_verified:
        ip_address = get_client_ip(request)
        cache.delete(ip_address)
        return Response({'message': message}, status=status.HTTP_200_OK)
    else:
        return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)
