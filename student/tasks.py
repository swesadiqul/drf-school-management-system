from celery import Celery
from django.utils import timezone
from .models.fees import FeesMaster

app = Celery('student')

# celery -A core beat
# celery -A core worker --loglevel=info
# redis-server
# celery -A core worker --loglevel=info --pool=solo


@app.task
def apply_fines():
    current_time = timezone.now()
    overdue_fees = FeesMaster.objects.filter(due_date__lt=current_time)

    for fee in overdue_fees:
        if fee.fine_type == 'Fixed':
            fee.amount += fee.fine_amount
        elif fee.fine_type == 'Percentage':
            fine_percentage = fee.fine_percentage / 100
            fee.amount += fee.amount * fine_percentage
        fee.save()

