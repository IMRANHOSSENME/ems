from django.shortcuts import render , redirect , get_object_or_404
from events.models import Event, Category , RSVP
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.views import is_admin, is_organizer, is_participant

# Create Event
@login_required
def create_event(request):
    # Role check Admin and Organizer
    if is_admin(request.user):
        base_template = "admin/header.html"
    elif is_organizer(request.user):
        base_template = "organizer/base.html"
    else:
        return redirect('/404')
    

    users = User.objects.all()
    CONTEXT = {
        'users': users,
        'base_template': base_template,
    }
    if request.method == 'POST':
        event_name = request.POST.get('name')
        event_description = request.POST.get('description')
        event_datetime = request.POST.get('datetime')
        event_location = request.POST.get('location')
        event_category = request.POST.get('category_name')
        category_description = request.POST.get('category_description')
        image = request.FILES.get('image')
        participants_ids = request.POST.getlist('participants')

        if event_name and event_datetime and event_location and event_category:
            category_obj, _ = Category.objects.get_or_create(
                name=event_category,
                defaults={'description': category_description}
            )

            event = Event.objects.create(
                name=event_name,
                image=image,
                date=event_datetime,
                location=event_location,
                description=event_description,
                category=category_obj,
                organizer=request.user,
            )

            # Add participants via RSVP
            for user_id in participants_ids:
                try:
                    user = User.objects.get(id=user_id)
                    RSVP.objects.create(event=event, user=user, status=RSVP.GOING)
                except User.DoesNotExist:
                    continue

            messages.success(request, 'Event created successfully!')
            return redirect('/dashboard')
        else:
            messages.error(request, 'Please fill in all required fields.')

    return render(request, 'create_event.html', CONTEXT)


#Edit Event
@login_required
def edit_event(request, event_id):
     # Role check Admin and Organizer
    if is_admin(request.user):
        base_template = "admin/header.html"
    elif is_organizer(request.user):
        base_template = "organizer/base.html"
    else:
        return redirect('/404')

    event = Event.objects.get(id=event_id)
    users = User.objects.all()
    if request.method == 'POST':
        event_name = request.POST.get('event_name')
        event_description = request.POST.get('event_description')
        event_datetime = request.POST.get('event_datetime')
        event_location = request.POST.get('event_location')
        event_category = request.POST.get('event_category')
        image = request.FILES.get('image')
        participants_ids = request.POST.getlist('participants')

        if event_name and event_datetime and event_location and event_category:
            category_obj, _ = Category.objects.get_or_create(
                name=event_category
            )

            event.name = event_name
            if image:
                event.image = image
            event.date = event_datetime
            event.location = event_location
            event.description = event_description
            event.category = category_obj
            event.save()

            # Update participants via RSVP
            existing_rsvps = RSVP.objects.filter(event=event)
            existing_user_ids = list(existing_rsvps.values_list('user_id', flat=True))
            print("Existing User IDs:", existing_user_ids)
            # Add new participants
            for user_id in participants_ids:
                print("Participant ID:", user_id)
                if int(user_id) not in existing_user_ids:
                    try:
                        user = User.objects.get(id=user_id)
                        RSVP.objects.create(event=event, user=user, status=RSVP.GOING)
                    except User.DoesNotExist:
                        continue

            # Remove unselected participants
            for rsvp in existing_rsvps:
                if str(rsvp.user.id) not in participants_ids:
                    rsvp.delete()

            messages.success(request, 'Event updated successfully!')
            return redirect('/dashboard')
        else:
            messages.error(request, 'Please fill in all required fields.')
    selected_participants = list(RSVP.objects.filter(event=event).values_list('user_id', flat=True))

    context = {
        'event': event,
        'users': users,
        'selected_participants': selected_participants,
        'base_template': base_template,
    }
    return render(request, 'edit_event.html', context)



#Event Details
def event_details(request, event_id):
     # Role check Admin and Organizer
    if is_admin(request.user):
        print("Unauthorized access attempt by user:Admin")
        base_template = "admin/header.html"
    elif is_organizer(request.user):
        print("Unauthorized access attempt by user:Organizer")
        base_template = "organizer/base.html"
    else:
        return redirect('/404')
    

    event = Event.objects.get(id=event_id)
    rsvps = RSVP.objects.filter(event=event)
    going_count = rsvps.filter(status=RSVP.GOING).count()
    interested_count = rsvps.filter(status=RSVP.INTERESTED).count()
    user_rsvp = None
    if request.user.is_authenticated:
        try:
            user_rsvp = RSVP.objects.get(event=event, user=request.user)
        except RSVP.DoesNotExist:
            user_rsvp = None

    CONTEXT={
        'event': event,
        'going_count': going_count,
        'interested_count': interested_count,
        'user_rsvp': user_rsvp,
        'base_template': base_template,
    }
    return render(request, 'event_details.html', CONTEXT)


#Delete Event
@login_required
def delete_event(request, event_id):
     # Role check Admin and Organizer
    if is_admin(request.user):
        base_template = "admin/header.html"
    elif is_organizer(request.user):
        base_template = "organizer/base.html"
    else:
        return redirect('/404')
    

    event = Event.objects.get(id=event_id)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted successfully!')
        return redirect('/dashboard')
    



# Create Category by Admin and Organizer
@login_required(redirect_field_name=None, login_url='/signin/')
def create_category(request):
     # Role check Admin and Organizer
    if is_admin(request.user):
        base_template = "admin/header.html"
    elif is_organizer(request.user):
        base_template = "organizer/base.html"
    else:
        return redirect('/404')


    if request.method == 'POST':
        category_name = request.POST.get('name')
        category_description = request.POST.get('description')
        created_by = request.user
        if category_name and category_description:
            Category.objects.create(name=category_name, description=category_description, created_by=created_by)
            messages.success(request, 'Category created successfully.')
            return redirect('/dashboard')
        else:
            messages.error(request, 'Please fill in all fields.')
    return render(request, 'create_category.html', {'base_template': base_template})

# Edit Category by Admin and Organizer
@login_required(redirect_field_name=None, login_url='/signin/')
def edit_category(request, category_id):
     # Role check Admin and Organizer
    if is_admin(request.user):
        base_template = "admin/header.html"
    elif is_organizer(request.user):
        base_template = "organizer/base.html"
    else:
        return redirect('/404')
    

    category = Category.objects.get(id=category_id)

    if request.method == 'POST':
        category.name = request.POST.get('name', category.name)
        category.description = request.POST.get('description', category.description)
        category.save()
        messages.success(request, 'Category updated successfully.')
        return redirect('/dashboard')

    return render(request, 'edit_category.html', {'category': category, 'base_template': base_template})

# Delete Category by Admin and Organizer
@login_required(redirect_field_name=None, login_url='/signin/')
def delete_category(request, category_id):
     # Role check Admin and Organizer
    if is_admin(request.user):
        base_template = "admin/header.html"
    elif is_organizer(request.user):
        base_template = "organizer/base.html"
    else:
        return redirect('/404')
    
    category = Category.objects.get(id=category_id)
    category.delete()
    messages.success(request, 'Category deleted successfully.')
    return redirect('/dashboard')


# RSVP to Event
@login_required
def rsvp_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        print("RSVP status received:", status)
        # Validate status
        rsvp, created = RSVP.objects.get_or_create(event=event, user=request.user)
        if rsvp.status == RSVP.GOING or rsvp.status == RSVP.INTERESTED:
            messages.error(request, 'You have already registered for this event.')
        else:
            rsvp.status = status
            rsvp.save()
            messages.success(request, f'You have marked yourself as {status} for this event.')
    return redirect('/dashboard')
