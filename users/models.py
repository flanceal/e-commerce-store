from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.utils.timezone import now


# Create your models here.
class User(AbstractUser):
    image = models.ImageField(upload_to='users/', null=True, blank=True)
    is_verified_email = models.BooleanField(default=False)


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def __str__(self):
        return f"EmailVerification object for {self.user.email}"

    def send_verification_email(self):
        link = reverse('users:email-verification', kwargs={'email': self.user.email, 'code': self.code})
        verification_link = f"{settings.DOMAIN_NAME}{link}"
        subject = f"Please complete the email verification process"
        message = f"{self.user.username}, Please verify your email to complete the registration process." \
                  f"Click on the link provided in the email to verify your account\n{verification_link}"

        send_mail(
            subject=subject,
            message=message,
            from_email="from@example.com",
            recipient_list=[self.user.email],
            fail_silently=False,
        )

    def is_expired(self):
        return now() >= self.expiration



