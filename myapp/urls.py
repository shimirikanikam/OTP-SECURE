from django.urls import path
from .views import request_otp_view, verify_otp_view

urlpatterns = [
    path('request_otp/', request_otp_view, name='request_otp'),
    path('verify_otp/', verify_otp_view, name='verify_otp'),
]