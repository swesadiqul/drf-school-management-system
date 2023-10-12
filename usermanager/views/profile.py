from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login, logout
from ..serializers.profile import ChangePasswordSerializer
from drf_spectacular.utils import extend_schema

CustomUser = get_user_model()

class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({
            'status': status.HTTP_200_OK,
            'message': 'User successfully logout',
        })

@extend_schema(
    request=ChangePasswordSerializer,
    methods=['POST'],
    description='API endpoint to change the user password. '
                'This endpoint allows an authenticated user to change their password. '
                'The old password, along with the new password and confirmation, is required for this operation. '
                'The new password must meet certain requirements defined by the system.'
)
class ChangePasswordAPIView(APIView):
    """
    API endpoint to change the user password.
    """
    permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTAuthentication]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = CustomUser.objects.get(id=request.user.id)
            if user.check_password(serializer.data.get('old_password')):
                user.set_password(serializer.data.get('new_password'))
                user.save()
                return Response({'status': 'Password changed successful.'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Wrong password.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       