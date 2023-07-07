from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

@receiver(user_logged_in)
def send_login_notification(user, **kwargs):
    subject = 'Login Notification'
    message = f'Hello {user.username}, you have successfully logged in to your account.'
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [user.email]
 
    send_mail(subject, message, from_email, to_email)
