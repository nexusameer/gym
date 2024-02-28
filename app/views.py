from django.shortcuts import render, redirect,HttpResponse
from .forms import UserProfileForm
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from datetime import datetime, time
from django.contrib import messages
from django.utils import timezone

@login_required(login_url='loginuser')
def buyplan(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.is_subscription_active():
            messages.warning(request, 'You already have an active subscription.')
            return redirect('viewplan')  # Redirect to viewplan or another appropriate page
    except UserProfile.DoesNotExist:
        pass  # The user doesn't have a UserProfile yet, so they can proceed to buy a plan

    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            user_profile_data = form.cleaned_data
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)
            user_profile.membership_plan = user_profile_data['membership_plan']
            user_profile.membership_start_date = user_profile_data['membership_start_date']
            
            # Update membership_expiry_date based on the new subscription
            if user_profile.membership_plan and hasattr(user_profile.membership_plan, 'duration_months'):
                user_profile.membership_expiry_date = user_profile.membership_start_date + timedelta(days=30 * user_profile.membership_plan.duration_months)
            
            user_profile.save()
            messages.success(request, 'Plan bought successfully!')
            return redirect('viewplan')  # Redirect to the user's plan view page
    else:
        form = UserProfileForm()
    
    return render(request, 'buyplan.html', {'form': form})


@login_required(login_url='loginuser')
def viewplan(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        subscription_active = user_profile.is_subscription_active()
    except UserProfile.DoesNotExist:
        # If UserProfile doesn't exist, create one and set subscription_active to False
        user_profile = UserProfile.objects.create(user=request.user)
        subscription_active = False

    return render(request, 'viewplan.html', {'user_profile': user_profile, 'subscription_active': subscription_active})

# Create your views here.
def index(request):
    if request.user.is_authenticated and request.user.userprofile.is_subscription_expired():
        messages.error(request, "Your subscription has expired. Please renew your subscription.")
    return render(request, 'index.html')

def service(request):
    plan = MembershipPlan.objects.all()
    context = {'plan': plan}
    return render(request, 'service.html', context)

def success_page(request):
    return render(request, 'success_page.html')


# Authentications
def loginuser(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.success(request, ("There was an error in logging in, try again"))
            return redirect('loginuser')
    else:
        return render(request, 'loginuser.html')

def logoutuser(request):
    logout(request)
    return redirect('index')

# views.py

# ... Existing imports ...

# Modify your register user function to handle UserProfile
def registeruser(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Create a UserProfile for the user
            UserProfile.objects.create(user=user)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Registration successful. You are now logged in.')
            return redirect('index')
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')

    context = {'form': form}
    return render(request, 'registeruser.html', context)

