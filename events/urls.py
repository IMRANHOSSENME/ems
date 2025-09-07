from django.urls import path
from events.views import create_event, edit_event ,event_details , delete_event ,create_category, edit_category, delete_category ,rsvp_event

urlpatterns = [
    path('events/create/', create_event, name='create_event'),
    path('events/edit/<int:event_id>/', edit_event, name='edit_event'),
    path('events/details/<int:event_id>/', event_details, name='event_details'),
    path('events/delete/<int:event_id>/', delete_event, name='delete_event'),
    path('categories/create/', create_category, name='create_category'),
    path('categories/edit/<int:category_id>/', edit_category, name='edit_category'),
    path('categories/delete/<int:category_id>/', delete_category, name='delete_category'),
    path('events/interested/<int:event_id>/', rsvp_event, name='rsvp_event'),
        
]
