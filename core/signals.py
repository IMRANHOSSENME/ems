from django.db.models.signals import post_save
from accounts.models import MyUser as User
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import Group

@receiver(post_save, sender=User)
def default_user_role(sender, instance, created, **kwargs):
    if created:
        # Assign default role
        participant_group, created_group = Group.objects.get_or_create(name='Participant')
        instance.groups.add(participant_group)
        instance.save()