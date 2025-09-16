from django.db.models.signals import post_save
from accounts.models import MyUser
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator

@receiver(post_save, sender=MyUser)
def send_account_activation_email(sender, instance, created, **kwargs):
    print("Signal triggered for user:", instance.email)
    if created and not instance.is_active:
        token = default_token_generator.make_token(instance)
        activation_link = f"{settings.FRONTEND_URL}/activate/{instance.pk}/{token}/"

        subject = 'Activate Your Account'
        message = render_to_string('emails/activation_email.html', {
            'user': instance,
            'activation_link': activation_link,
        })
        print("Sending activation email to:", instance.email)
        print("Email subject:", subject)
        send_mail(
            subject=subject,
            message='', 
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.email],
            fail_silently=False,
            html_message=message
        )