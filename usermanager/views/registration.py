from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
import datetime
import json
from django.db.models import Q
from drf_spectacular.utils import extend_schema
from ..utils import send_otp_via_email, generate_otp
from ..serializers.registration import SignupSerializer, VerifyOTPSerializer


CustomUser = get_user_model()

@extend_schema(
    request=SignupSerializer,
    methods=['POST'],
    description='API endpoint to sign up a new user. '
                'This endpoint allows a user to register with their email and password. '
                'A verification code will be sent to the provided email address for account verification. '
                'The user needs to input the verification code to complete the registration process. '
                'The password must meet certain requirements defined by the system.'
)
class SignupAPIView(APIView):
    """
    API endpoint to sign up a new user.
    """
    def post(self, request):
        # Get the user's data from the request
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            email = request.data.get('email')
            password2 = request.data.get('password2')

            try:
                user = CustomUser.objects.get(email=email)
                return Response({'error': 'User already exists.'}, status=400)
            except ObjectDoesNotExist:
                pass

            # Generate a new OTP
            secret, otp = generate_otp()

            otp_expire_time = datetime.datetime.now() + datetime.timedelta(minutes=1)
            otp_expire_time_str = otp_expire_time.strftime('%Y-%m-%d %H:%M:%S')
            # Serialize the string using JSON
            otp_expire_time_json = json.dumps(
                {'timestamp': otp_expire_time_str})

            # Save the secret key, phone_number, email, otp_expire_time and OTP in the user's session
            request.session['otp_secret'] = secret
            request.session['otp'] = otp
            request.session['email'] = email
            request.session['otp_expire_time'] = otp_expire_time_json
            request.session['password2'] = password2

            # Send the OTP to the user's phone number using your preferred method
            send_otp_via_email(email, otp)

            return Response({'success': 'OTP has been sent.'}, status=200)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=VerifyOTPSerializer,
    methods=['POST'],
    description='API endpoint to verify a user\'s sign-up using an OTP (One-Time Password). '
                'The user must provide their email and the OTP sent to their email during the sign-up process. '
                'If the OTP is valid and matches the one sent during sign-up, '
                'the user account will be verified and created. '
                'If the OTP is invalid or has expired, an error will be returned.'
)
class VerifySingupOTPView(APIView):
    """
    API endpoint to verify a user's sign-up using an OTP.
    """
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            # Get the user's data from the request
            email = request.data.get('email')
           
            otp = request.data.get('otp')
            user_qs = CustomUser.objects.filter(email=email)
            
            if user_qs.exists():
                return Response({'error': 'User already verified.'}, status=400)

            elif not user_qs.exists():
                # Get the secret key, email, and OTP expiry time from the user's session
                otp_secret = request.session.get('otp_secret')
                otp = request.session.get('otp')
                email = request.session.get('email')
                otp_expire_time = request.session.get('otp_expire_time')
                password2 = request.session.get('password2')
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
                    request.session['password2'] = password2
                    send_otp_via_email(email, otp)

                    return Response({'error': 'OTP has expired. A new OTP has been sent.'}, status=400)

                elif request.session['otp'] == otp:
                    # Create the user
                    user = CustomUser.objects.create(email=email)
                    user.set_password(password2)
                    user.save()

                    # Clear the session data
                    del request.session['otp_secret']
                    del request.session['otp']
                    del request.session['email']
                    del request.session['otp_expire_time']
                    del request.session['password2']

                    return Response({'success': 'User has been created.'}, status=200)
                else:
                    return Response({'message': 'Wrong OTP'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            
            
