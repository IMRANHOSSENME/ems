from django.shortcuts import render , redirect ,HttpResponse
from django.contrib.auth.models import User
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
from accounts.views import is_admin, is_organizer ,is_participant,dashboard_redirect
from django.contrib.auth.decorators import login_required

#Home page
def home(request):
    events = Event.objects.select_related('category').all().order_by('-date')
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


#Login page
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('/dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
        return render(request, 'signin.html')
    # For GET requests, render the login form
    return render(request, 'signin.html')


#Registration page
def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('signup')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return redirect('signup')

        if password == confirm_password:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                is_active=False  # User is inactive until Email verification
            )
            
            messages.success(request, 'Registration successful! Please verify your email to activate your account.')
            return redirect('signin')
        else:
            messages.error(request, 'Passwords do not match.')

    return render(request,'signup.html')



# 404 Error page
def preview_404(request):
    return render(request, '404.html', {'exception': None}, status=404)


def signout(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('signin')


# About page
def about(request):
    return HttpResponse("This is the about page.")

# Events page
def events(request):
    return HttpResponse("This is the events page.")

# Contact page
def contact(request):
    return HttpResponse("This is the contact page.")


