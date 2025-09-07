from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator

@receiver(post_save, sender=User)
def send_account_activation_email(sender, instance, created, **kwargs):
    if created and not instance.is_active:
        token = default_token_generator.make_token(instance)
        activation_link = f"{settings.FRONTEND_URL}/activate/{instance.pk}/{token}/"

        subject = 'Activate Your Account'
        message = render_to_string('emails/activation_email.html', {
            'user': instance,
            'activation_link': activation_link,
        })
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [instance.email],
            fail_silently=False,
        )