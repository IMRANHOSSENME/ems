from accounts.models import MyUser as User
from django.db import models

# Event model
class Event(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/events/')
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='events')
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events',default=1)
    participants = models.ManyToManyField(User, through='RSVP', related_name='events_participated')

    def __str__(self):
        return self.name


# Category model
class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories', default=1)

    def __str__(self):
        return self.name

# RSVP model
class RSVP(models.Model):
    GOING = "going"
    INTERESTED = "interested"
    STATUS_CHOICES = [
        (GOING, "Going"),
        (INTERESTED, "Interested"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rsvps')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='rsvps')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=GOING)

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        return f"{self.user.username} - {self.event.name}"
