from django.urls import path
from core.views import home, signin, signup, preview_404 ,signout , about, events, contact

urlpatterns = [
    path('', home, name='home'),
    path('signin/', signin, name='signin'),
    path('signup/', signup, name='signup'),
    path('404/', preview_404, name='preview_404'),
    path('signout/', signout, name='signout'),
    path('about/', about, name='about'),
    path('events/', events, name='events'),
    path('contact/', contact, name='contact'),
]
