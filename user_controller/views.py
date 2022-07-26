
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login as auth_login, logout as auth_logout
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.db.models import Q

from .forms import SignupForm, LoginForm, ProfileForm
from .decorators import login_required_with_feedback
from .models import CustomUser, UserProfile, FriendRequest, Friends


User = get_user_model()
  
 
def index(request):
    """Home page view"""

    return render(request, 'assessment/index.html')

def signup(request):
    """Sign up view"""
   
    signup_form = SignupForm()

    if request.method == 'POST':
        signup_form = SignupForm(request.POST)

        if signup_form.is_valid():
            user = signup_form.save(commit=False)
            user.is_active = True
            user.save()
            messages.success(request, 'User created successfully')
            return HttpResponseRedirect(reverse('login'))     
    ctx = {
        'signup_form': signup_form
    }
    return render(request, 'assessment/signup.html', ctx)

def login(request):
    """Sign in view"""

    login_form = LoginForm()
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        
        if login_form.is_valid():
            user = authenticate(request, **login_form.cleaned_data)
            if user:
                auth_login(request, user)
                messages.success(request, 'User logged in successfully')
                return HttpResponseRedirect(reverse('home'))
            else:
                login_form.add_error(None, ValidationError('Login Failed. Email and/or password is incorrect.'))
    ctx = {
        'login_form': login_form
    }
    return render(request, 'assessment/login.html', ctx)

def logout(request):
    """logout view"""

    auth_logout(request)
    return HttpResponseRedirect(reverse('login'))

@login_required_with_feedback
def profile_view(request):
    """Profile view"""

    profile = UserProfile.objects.get(id=request.user.id)
    profile_form = ProfileForm(instance=profile)
    ctx = {
        'profile': profile,
        "profile_form": profile_form
    }
    return render(request, 'assessment/profile.html', ctx)

@login_required_with_feedback
def add_profile_photo(request):
    """Edit profile view to upload picture. """

    profile = UserProfile.objects.get(id=request.user.id)
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
        
            profile_form.save()
            messages.success(request, 'Profie updated successfully')
            return HttpResponseRedirect(reverse('profile'))
        messages.info(request, 'Something went wrong. Try again.')
        return HttpResponseRedirect(reverse('profile'))      

@login_required_with_feedback
def search_users(request):
    """Search for users view."""

    if request.method == "POST":
        query = request.POST.get("search")
        if query:
            users = CustomUser.objects.filter(Q(username__icontains=query)).exclude(
                            username=request.user.username).distinct()
            if users:
                ctx = {
                    "users": users
                }
                return render(request, 'assessment/search.html', ctx)
            messages.info(request, 'No friends with such username')
    
        return render(request, 'assessment/index.html')
    else:
        return render(request, 'assessment/index.html')


@login_required_with_feedback
def add_friend(request, user_id):
    """Send friend request view."""

    from_user = request.user
    
    to_user = get_object_or_404(CustomUser, pk=user_id)

    can_add_friend = Friends.can_add_friend(to_user)
    if can_add_friend:
        can_send_request = FriendRequest.can_send_request(to_user)
        if can_send_request: 
            try:
                FriendRequest.objects.create(from_user=from_user, to_user=to_user)
            except IntegrityError:
                pass
            messages.success(request, 'Friend request sent.')
            return HttpResponseRedirect(reverse('home')) 
        messages.info(request, 'Friend request already sent.')
        return HttpResponseRedirect(reverse('home'))    
    else:
        messages.info(request, 'User is already a friend.')
        return HttpResponseRedirect(reverse('home'))    
    

@login_required_with_feedback
def friend_request_view(request):
    """View pending friend request received view."""

    user = request.user
    
    friend_requests=None
    if FriendRequest.objects.filter(to_user=user).exists():
        friend_requests =FriendRequest.objects.filter(to_user=user)
    ctx = {
        "friend_requests":friend_requests
    }
    return render(request, 'assessment/friend_request.html', ctx)
    
@login_required_with_feedback
def accept_friend_request(request, friend_request_id):
    """Accept a friend request view."""

    friend_request = get_object_or_404(FriendRequest, pk=friend_request_id)
    if CustomUser.objects.filter(username=friend_request.to_user.username).exists():
        friend = CustomUser.objects.get(username=friend_request.to_user.username)

        if friend != request.user:
            messages.info(request, 'You are not authorized to accept this request')
            return HttpResponseRedirect(reverse('home')) 
        friend_request.accept()
        #delete friend request instance after accept
        friend_request.delete()
        messages.success(request, 'Friend request accepted successfully')
        return HttpResponseRedirect(reverse('friends')) 
    else:
        messages.info(request, 'Something went wrong. Try again.')
        return HttpResponseRedirect(reverse('home')) 

@login_required_with_feedback
def reject_friend_request(request, friend_request_id):
    """Reject a friend request view."""

    friend_request = get_object_or_404(FriendRequest, pk=friend_request_id)
    if CustomUser.objects.filter(username=friend_request.to_user.username).exists():
        friend = CustomUser.objects.get(username=friend_request.to_user.username)

        if friend != request.user:
            messages.info(request, 'You are not authorized to accept this request')
            return HttpResponseRedirect(reverse('home')) 
        friend_request.reject()
        #delete friend request instance after reject
        friend_request.delete()
        messages.success(request, 'Friend request rejected')
        return HttpResponseRedirect(reverse('friends')) 
    else:
        messages.info(request, 'Something went wrong. Try again.')
        return HttpResponseRedirect(reverse('home')) 

@login_required_with_feedback
def friends_view(request):
    """Friends list view."""

    profile = UserProfile.objects.get(user=request.user)
    friends = profile.friends.all()
    ctx = {
        "friends": friends
    }
    return render(request, 'assessment/friends.html', ctx)
