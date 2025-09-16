from django.urls import path
from events.views import CreateEventView, EditEventView ,EventDetailsView , DeleteEventView ,CreateCategoryView, EditCategoryView, DeleteCategoryView ,RsvpEventView

urlpatterns = [
    path('events/create/', CreateEventView.as_view(), name='create_event'),
    path('events/edit/<int:event_id>/', EditEventView.as_view(), name='edit_event'),
    path('events/details/<int:event_id>/', EventDetailsView.as_view(), name='event_details'),
    path('events/delete/<int:event_id>/', DeleteEventView.as_view(), name='delete_event'),
    path('categories/create/', CreateCategoryView.as_view(), name='create_category'),
    path('categories/edit/<int:category_id>/', EditCategoryView.as_view(), name='edit_category'),
    path('categories/delete/<int:category_id>/', DeleteCategoryView.as_view(), name='delete_category'),
    path('events/interested/<int:event_id>/', RsvpEventView.as_view(), name='rsvp_event'),

]
