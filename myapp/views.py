from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services import OTPService
import base64
from .serializers import VerifyOTPSerializer
from .utils import mobile_number_pattern_validation, otp_number_pattern_validation,mobile_number_decoder


@api_view(['POST'])
def request_otp_view(request):
    mobile_number_base64 = request.data.get('mobile_number')
    
    mobile_number= mobile_number_decoder(mobile_number_base64)
    if not mobile_number:
        return Response({'error': 'Invalid base64 encoding or decoding error.'}, status=400)
    
    if not mobile_number_pattern_validation(mobile_number):
        return Response({'error': 'Please provide a valid 10-digit mobile number starting with a digit between 6 and 9.'}, status=400)
    mobile_number_pattern_validation(mobile_number)

    otp, message = OTPService.request_otp(mobile_number)
    if not otp:
        return Response({'error': message}, status=429)
    

    return Response({'otp': otp, 'message': message}, status=200)

@api_view(['POST'])
def verify_otp_view(request):
    serializer = VerifyOTPSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)
    
    mobile_number_base64 = serializer.validated_data['mobile_number_base64']
    user_otp = serializer.validated_data['user_otp']

    mobile_number= mobile_number_decoder(mobile_number_base64)
    if not mobile_number:
        return Response({'error': 'Invalid base64 encoding or decoding error.'}, status=400)
    if not mobile_number_pattern_validation(mobile_number):
        return Response({'error': 'Please provide a valid 10-digit mobile number starting with a digit between 6 and 9.'}, status=400)
    mobile_number_pattern_validation(mobile_number)

    if not otp_number_pattern_validation(user_otp):
        return Response({'error': 'Please provide a valid 6-digit OTP.'}, status=400)
    otp_number_pattern_validation(user_otp)

    is_verified, message = OTPService.verify_otp(mobile_number, user_otp)
    if is_verified:
        return Response({'message': message}, status=200)
    else:
        return Response({'error': message}, status=400)
