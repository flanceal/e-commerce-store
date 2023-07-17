from celery import shared_task

from users.models import EmailVerification, User

from django.utils.timezone import now
import uuid
from datetime import timedelta


@shared_task
def send_email_verification(self, user_id):
    user = User.objects.get(id=user_id)
    expiration = now() + timedelta(hours=48)
    code = uuid.uuid4()
    record = EmailVerification.objects.create(code=code, user=user, expiration=expiration)
    record.send_verification_email()

