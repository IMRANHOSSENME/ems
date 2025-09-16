from django.urls import path
from core.views import home, SigninView, SignupView, preview_404 , about, events, contact ,SignoutView , CustomPasswordResetView , CustomPasswordDoneView , CustomPasswordConfirmView , CustomPasswordCompleteView

urlpatterns = [
    path('', home, name='home'),
    path('signin/', SigninView.as_view(), name='signin'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('404/', preview_404, name='preview_404'),
    path('signout/', SignoutView.as_view(), name='signout'),
    path('about/', about, name='about'),
    path('events/', events, name='events'),
    path('contact/', contact, name='contact'),
    path('forgate-password/', CustomPasswordResetView.as_view(), name='forgate_password'),
    path('reset/<uidb64>/<token>/', CustomPasswordConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordCompleteView.as_view(), name='password_reset_complete'),
    path('reset/sent/', CustomPasswordDoneView.as_view(), name='password_reset_done'),
    # path('test-email/', test_email, name='test_email'),  # New URL pattern for testing email

]
