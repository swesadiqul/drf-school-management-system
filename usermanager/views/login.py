from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
import datetime
from django.utils import timezone
import json
from ..serializers.login import LoginSerializer, ResetPasswordSerializer, VerifyResetPasswordOTPSerializer, ResetPasswordConfirmSerializer
from ..utils import generate_otp, send_otp_via_email

CustomUser = get_user_model()


class LoginAPIView(APIView):

    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid():
                email = serializer.data['email']
                password = serializer.data['password']

                user = authenticate(email=email, password=password)

                if user is None:
                    return Response({
                        'status': status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
                        'message': 'Invalid email or password.',
                        'error': serializer.errors
                    })

                refresh = RefreshToken.for_user(user)
                login(request, user)
                return Response({
                    'status': status.HTTP_200_OK,
                    'message': 'User successfully login',
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                })

            return Response({
                'status': status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
                'message': 'Invalid email or password.',
                'error': serializer.errors
            })
        except Exception as e:
            print(e)

        return Response({
            'status': status.HTTP_404_NOT_FOUND,
            'message': 'Email or password is invalid.',
        })


class ResetPasswordAPIView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = ResetPasswordSerializer(data=request.data)

        if serializer.is_valid():
            email = request.data.get('email')

            user_qs = CustomUser.objects.filter(email=email)

            if user_qs.exists():
                # Generate a new OTP
                secret, otp = generate_otp()

                otp_expire_time = datetime.datetime.now() + datetime.timedelta(minutes=1)
                otp_expire_time_str = otp_expire_time.strftime(
                    '%Y-%m-%d %H:%M:%S')
                # Serialize the string using JSON
                otp_expire_time_json = json.dumps(
                    {'timestamp': otp_expire_time_str})

                # Save the secret key, phone_number, email, otp_expire_time and OTP in the user's session
                request.session['email'] = email
                request.session['otp_secret'] = secret
                request.session['otp'] = otp
                request.session['otp_expire_time'] = otp_expire_time_json
                # Send the OTP to the user's email using your preferred method
                send_otp_via_email(email, otp)

                return Response({'success': 'OTP has been sent.'}, status=200)
            else:
                return Response({'error': 'User not found.'}, status=400)

        return Response({
            'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'message': 'Internal Server Error.',
        })


class VerifyResetPasswordOTPAPIView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = VerifyResetPasswordOTPSerializer(data=request.data)
        if serializer.is_valid():
            # Get the user's data from the request
            otp = request.data.get('otp')
            email = request.session.get('email')
            user_qs = CustomUser.objects.filter(email=email)

            if user_qs.exists():
                # Get the secret key, email, and OTP expiry time from the user's session
                otp_secret = request.session.get('otp_secret')
                otp = request.session.get('otp')
                email = request.session.get('email')
                otp_expire_time = request.session.get('otp_expire_time')
                recent_time = datetime.datetime.now()
                # Convert datetime object to string
                recent_time_str = recent_time.strftime('%Y-%m-%d %H:%M:%S')

                # Serialize the string using JSON
                recent_time_json = json.dumps(
                    {'timestamp': recent_time_str})

                # Check if the OTP has expired
                if recent_time_json > otp_expire_time:
                    # Generate a new OTP
                    secret, otp = generate_otp()

                    otp_expire_time = datetime.datetime.now() + datetime.timedelta(minutes=1)
                    otp_expire_time_str = otp_expire_time.strftime(
                        '%Y-%m-%d %H:%M:%S')
                    # Serialize the string using JSON
                    otp_expire_time_json = json.dumps(
                        {'timestamp': otp_expire_time_str})

                    # Save the secret key and OTP in the user's session
                    request.session['otp_secret'] = secret
                    request.session['otp'] = otp
                    request.session['email'] = email
                    request.session['otp_expire_time'] = otp_expire_time_json
                    send_otp_via_email(email, otp)

                    return Response({'error': 'OTP has expired. A new OTP has been sent.'}, status=400)

                elif request.session['otp'] == otp:

                    # Clear the session data
                    del request.session['otp_secret']
                    del request.session['otp']
                    del request.session['otp_expire_time']

                    return Response({'success': 'User credentials verified.'}, status=200)

            elif not user_qs.exists():
                return Response({'error': 'User do not exist.'}, status=400)

        return Response({
            'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'message': 'Internal Server Error.',
        })


class ResetPasswordConfirmAPIView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = ResetPasswordConfirmSerializer(data=request.data)

        email = request.session.get('email')
        password = serializer.validated_data['password']

        user = CustomUser.objects.filter(email=email).first()
        if not user:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        user.set_password(password)
        user.save()
        
        del request.session['email']

        return Response({'message': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)
