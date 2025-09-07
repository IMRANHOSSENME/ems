import token
from django.shortcuts import render, HttpResponse , redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.contrib.auth.models import Group , Permission
from events import models
from events.models import Event ,Category , RSVP
from django.db.models import Prefetch
from django.utils import timezone




#Account Activation Check
def activation(request , user_id, token):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Account activated successfully.')
        return redirect('/signin/')
    else:
        messages.error(request, 'Activation link is invalid or has expired.')
        return redirect('/signup/')
    

# Role Check Functions
def is_admin(user):
    return user.groups.filter(name='Admin').exists() or user.is_superuser

def is_organizer(user):
    return user.groups.filter(name='Organizer').exists()

def is_participant(user):
    return user.groups.filter(name='Participant').exists()

#Dashboards and User Management
def dashboard_redirect(request):
    if not request.user.is_authenticated:
        return redirect('/signin/')
    if is_admin(request.user):
        return redirect('/accounts/admin/dashboard')
    elif is_organizer(request.user):
        return redirect('/accounts/organizer/dashboard')
    elif is_participant(request.user):
        return redirect('/accounts/participant/dashboard')
    else:
        messages.error(request, 'No role assigned. Please contact admin.')
        return redirect('/signin')

# Create Roles
@login_required(redirect_field_name=None, login_url='/signin/')
def create_role(request):
    if not is_admin(request.user):
        print("Unauthorized access attempt by user:", request.user)
        return redirect('/404') 
    chosen_permissions = request.POST.getlist('chosenPermissions')
    permission = Permission.objects.all()
    if request.method == 'POST':
        role_name = request.POST.get('roleName')
        if role_name:
            role_name = role_name.strip()
        else:
            role_name = ''
        if Group.objects.filter(name=role_name).exists():
            messages.error(request, 'Role already exists.')
        else:
            group = Group(name=role_name)
            group.save()
            for perm_id in chosen_permissions:
                try:
                    perm = Permission.objects.get(id=perm_id)
                    group.permissions.add(perm)
                except Permission.DoesNotExist:
                    messages.error(request, f'Permission with id {perm_id} does not exist.')
            messages.success(request, 'Role created successfully.')
    return render(request, 'admin/create_role.html', {'permissions': permission})




#Admin Dashboard
@login_required(redirect_field_name=None, login_url='/signin/')
def admin_dashboard(request):
    if not is_admin(request.user):
        print("Unauthorized access attempt by user:", request.user)
        return redirect('/404')
    events = Event.objects.select_related('category', 'organizer').prefetch_related('participants').all().order_by('-date')
    total_events = events.count()
    upcoming_events = events.filter(date__gt=timezone.now()).count()
    completed_events = events.filter(date__lt=timezone.now()).count()
    today_events = events.filter(date=timezone.now().date())
    users = User.objects.all()
    catagorys = Category.objects.all()
    from django.db.models import Count

    total_events_interested = Event.objects.aggregate(total=Count('participants', distinct=True))['total']
    # all_going_users = User.objects.filter(rsvps__status='going').distinct()

    CONTEXT = {
        'events': events,
        'user': users,
        'catagorys': catagorys,
        'today_events': today_events,
        'total_events': total_events,
        'upcoming_events': upcoming_events,
        'completed_events': completed_events,
        'total_interested': total_events_interested
    }

    return render(request, 'admin/dashboard.html', CONTEXT)


# Organizer Dashboard
@login_required(redirect_field_name=None, login_url='/signin/')
def organizer_dashboard(request):
    if not is_organizer(request.user):
        print("Unauthorized access attempt by user:", request.user)
        return redirect('/404')

    events = Event.objects.filter(organizer=request.user).order_by('-date')
    categories = Category.objects.filter(created_by=request.user).distinct() | Category.objects.filter(events__organizer=request.user).distinct()

    return render(request,'organizer/dashboard.html', {'events': events, 'categories': categories})


#Participant Dashboard

@login_required(redirect_field_name=None, login_url='/signin/')
def participant_dashboard(request):
    if not is_participant(request.user):
        print("Unauthorized access attempt by user:", request.user)
        return redirect('/404')
    events = Event.objects.filter(participants=request.user).select_related('category', 'organizer').all().order_by('-date')
    print(events)
    return render(request,'participant/dashboard.html', {'events': events})


# Add User by Admin
@login_required(redirect_field_name=None, login_url='/signin/')
def add_user(request):
    if not is_admin(request.user):
        print("Unauthorized access attempt by user:", request.user)
        return redirect('/404')
    groups = Group.objects.all()
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('/accounts/admin/add-user')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('/accounts/admin/add-user')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_active=True
        )

        selected_groups = request.POST.getlist('groups')
        for group_id in selected_groups:
            try:
                group = Group.objects.get(id=group_id)
                user.groups.add(group)
            except Group.DoesNotExist:
                continue

        user.save()
        messages.success(request, 'User created successfully.')
        return redirect('/accounts/admin/dashboard')
    return render(request, 'admin/add_user.html', {'groups': groups})


# Edit User by Admin
@login_required(redirect_field_name=None, login_url='/signin/')
def edit_user(request, user_id):
    if not is_admin(request.user):
        print("Unauthorized access attempt by user:", request.user)
        return redirect('/404')
    user = User.objects.get(id=user_id)
    groups = Group.objects.all()

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.username = request.POST.get('username', user.username)

        #Account Status
        user.is_active = 'is_active' in request.POST
        user.is_staff = 'is_staff' in request.POST
        user.is_superuser = 'is_superuser' in request.POST


        #Role Update
        selected_groups = request.POST.getlist('groups')
        print("Selected groups:", selected_groups)
        user.groups.clear()
        for group_id in selected_groups:
            try:
                group = Group.objects.get(id=group_id)
                user.groups.add(group)
            except Group.DoesNotExist:
                continue
        user.save()
        messages.success(request, 'User updated successfully.')
        return redirect('/accounts/admin/dashboard')
    return render(request, 'admin/edit_user.html', {'user': user, 'groups': groups})


#Delete User by Admin
@login_required(redirect_field_name=None, login_url='/signin/')
def delete_user(request, user_id):
    if not is_admin(request.user):
        print("Unauthorized access attempt by user:", request.user)
        return redirect('/404')
    user = User.objects.get(id=user_id)
    user.delete()
    messages.success(request, 'User deleted successfully.')
    return redirect('/accounts/admin/dashboard')



