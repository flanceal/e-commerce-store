from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.urls import reverse
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
        print("Verification link:", verification_link)
        subject = "Please complete the email verification process"

        # Plain text content for email clients that don't support HTML
        plain_message = f"{self.user.username}, Please verify your email to complete the registration process. Click on the link provided in the email to verify your account: {verification_link}"

        html_message = f"""
        <html>
            <head>
                <style>
                    body {{ font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; background-color: #ECECEC; margin: 0; padding: 0; }}
                    .email-container {{ max-width: 550px; margin: 40px auto; background-color: white; box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-radius: 8px; overflow: hidden; }}
                    .email-header {{ background-color: #4A90E2; padding: 20px 30px; }}
                    .email-header h2 {{ color: white; margin: 0; font-size: 24px; }}
                    .email-body {{ padding: 30px; color: #333; }}
                    .email-body p {{ line-height: 1.5; font-size: 16px; }}
                    .button {{
                        background-color: #FF6F61; 
                        color: white; 
                        padding: 10px 15px; 
                        text-decoration: none; 
                        border-radius: 5px; 
                        font-size: 18px; 
                        display: inline-block; 
                        margin-top: 20px;
                    }}
                    .button:hover {{ background-color: #E55B4D; }}
                    .footer {{ background-color: #F5F5F5; color: #888; padding: 20px 30px; text-align: center; font-size: 14px; }}
                </style>
            </head>
            <body>
                <div class="email-container">
                    <div class="email-header">
                        <h2>Email Verification</h2>
                    </div>
                    <div class="email-body">
                        <p>Hi {self.user.username},</p>
                        <p>Thank you for registering with us. To complete your registration, please verify your email address by clicking the button below.</p>
                        <a href="http://{verification_link}" style="background-color: #FF6F61; color: white; padding: 10px 15px; text-decoration: none; border-radius: 5px; font-size: 18px; display: inline-block; margin-top: 20px; text-align: center;">
                            Verify Email
                        </a>
                       
                    </div>
                    <div class="footer">
                        &copy; {now().year} Fartanov. All Rights Reserved (Not really).
                    </div>
                </div>
            </body>
        </html>
        """

        # Create an EmailMultiAlternatives instance
        email = EmailMultiAlternatives(
            subject=subject,
            body=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            to=[self.user.email],
        )
        # Attach the HTML alternative content
        email.attach_alternative(html_message, "text/html")
        # Send the email
        email.send(fail_silently=False)

    def is_expired(self):
        return now() >= self.expiration
