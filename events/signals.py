
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from events.models import RSVP

@receiver(post_save, sender=RSVP)
def send_rsvp_confirmation(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        event = instance.event
        subject = f"RSVP Confirmation for {event.name}"
        message = f"Hello {user.username},\n\nThank you for your RSVP for {event.name}.\n\nBest regards,\nThe Events Team"
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )