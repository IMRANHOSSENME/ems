from urllib import request
from django.shortcuts import render , redirect ,HttpResponse
from accounts.models import MyUser as User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from events.models import Event
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from accounts.views import is_admin, is_organizer ,is_participant
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView ,LoginView
from django.views import View
from core.forms import UserRegistrationForm , UserSignInForm
from django.contrib.auth.views import PasswordResetView , PasswordResetConfirmView
from django.urls import reverse_lazy
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib import messages

#Home page
def home(request):
    events = Event.objects.select_related('category').all().order_by('-date')
    if not events.exists():
        CONTEXT = {'events': events}
        return render(request, 'home.html', CONTEXT)
    fast_event = events.first()
    today = timezone.now()
    fast_event_days_left = (fast_event.date - today).days
    fast_event_hours_left = (fast_event.date - today).seconds // 3600
    fast_event_minutes_left = (fast_event.date - today).seconds // 60 % 60
    fast_event_seconds_left = (fast_event.date - today).seconds % 60

    CONTEXT={
        'events': events,
        'fast_event': fast_event,
        'days_left': fast_event_days_left,
        'hours_left': fast_event_hours_left,
        'minutes_left': fast_event_minutes_left,
        'seconds_left': fast_event_seconds_left,
    }
    return render(request, 'home.html', CONTEXT)

# Registration page
class SignupView(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_active = False  # User is inactive until Email verification
            user.save()
            messages.success(request, 'Registration successful! Please verify your email to activate your account.')
            return redirect('signin')
        return render(request, 'signup.html', {'form': form})


# Signin page
class SigninView(LoginView):
    template_name = 'signin.html'
    redirect_authenticated_user = True
    form_class = UserSignInForm


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        return kwargs

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)

    def get_success_url(self):
        user = self.request.user
        if is_admin(user):
            return '/accounts/admin/dashboard/'
        elif is_organizer(user):
            return '/accounts/organizer/dashboard/'
        elif is_participant(user):
            return '/accounts/participant/dashboard/'
        return '/'

# Signout
class SignoutView(LogoutView):
    next_page = 'home'


# 404 Error page
def preview_404(request):
    return render(request, '404.html', {'exception': None}, status=404)

# Forgate password page
class CustomPasswordResetView(PasswordResetView):
    def send_mail(self, subject_template_name, email_template_name, context, from_email, to_email, html_email_template_name=None):
        _ = html_email_template_name
        subject = render_to_string(subject_template_name, context) if subject_template_name else ''
        subject = ''.join(subject.splitlines())
        body = render_to_string(email_template_name, context)
        email_message = EmailMultiAlternatives(subject, '', from_email, [to_email])
        email_message.attach_alternative(body, 'text/html')
        email_message.send()
    template_name = 'forgate_password.html'
    email_template_name = 'emails/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')

class CustomPasswordDoneView(PasswordResetView):
    template_name = 'password_reset_done.html'
    success_url = reverse_lazy('home')

class CustomPasswordConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

    new_password1_field = 'New Password'
    new_password2_field = 'Confirm New Password'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Your password has been reset successfully. You can now log in with your new password.')
        return response

class CustomPasswordCompleteView(PasswordResetView):
    template_name = 'password_reset_complete.html'
    success_url = reverse_lazy('home')


# About page
def about(request):
    return HttpResponse("This is the about page.")

# Events page
def events(request):
    return HttpResponse("This is the events page.")

# Contact page
def contact(request):
    return HttpResponse("This is the contact page.")


def test_email(request):
    subject = 'Test Email'
    message = 'This is a test email.'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = ['yogot80178@cspaus.com']

    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list,
        fail_silently=False,
    )

    return HttpResponse("Test email sent.")