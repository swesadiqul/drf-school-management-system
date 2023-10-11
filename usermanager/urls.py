from django.urls import path
from .views.registration import SignupAPIView, VerifySingupOTPView
from .views.login import LoginAPIView, ResetPasswordAPIView, VerifyResetPasswordOTPAPIView, ResetPasswordConfirmAPIView
from .views.profile import LogoutAPIView, ChangePasswordAPIView


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

app_name = 'usermanager'

#create url mapping
urlpatterns = [
    
    # Token 
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # User
    path('signup/', SignupAPIView.as_view(), name="signup"),
    path('verify-otp/', VerifySingupOTPView.as_view(), name="verify_signup_otp"),
    path('signin/', LoginAPIView.as_view(), name="signin"),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('change-password/', ChangePasswordAPIView.as_view(), name="change_password"),
    path('reset-password/', ResetPasswordAPIView.as_view(), name='reset_password'),
    path('reset-password-otp/', VerifyResetPasswordOTPAPIView.as_view(), name='verify_reset_otp'),
    path('reset-password-confirm/', ResetPasswordConfirmAPIView.as_view(), name='reset_password_confirm'),
    
]