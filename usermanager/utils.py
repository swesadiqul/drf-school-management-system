from django.core.mail import send_mail
from django.conf import settings
import pyotp

def send_otp_via_email(email, otp):
    subject = "Your account activation email."
    message = f"Your account activation OTP is {otp}"
    email_from = settings.DEFAULT_FROM_EMAIL
    send_mail(subject, message, email_from, [email])


def generate_otp():
    # Generate a random secret key
    secret = pyotp.random_base32()

    # Create an OTP object
    totp = pyotp.TOTP(secret, digits=4)

    # Generate the OTP
    otp = totp.now()

    return secret, otp
