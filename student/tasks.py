from celery import Celery, shared_task
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models.fees import FeesMaster

app = Celery('student')

# celery -A core beat
# celery -A core worker --loglevel=info
# redis-server
# celery -A core worker --loglevel=info --pool=solo


@app.task
def apply_fines_once():
    current_time = timezone.now()
    overdue_fees = FeesMaster.objects.filter(due_date__lt=current_time, fined=False)

    for fee in overdue_fees:
        if fee.fine_type == 'Fixed':
            fee.amount += fee.fine_amount
        elif fee.fine_type == 'Percentage':
            fine_percentage = fee.fine_percentage / 100
            fee.amount += fee.amount * fine_percentage

        # Mark the fee as fined so that it won't be fined again in the future
        fee.fined = True
        fee.save()


@shared_task
def send_email_to_student(email, subject, message):
    email_from = settings.DEFAULT_FROM_EMAIL
    send_mail(subject, message, email_from, [email])