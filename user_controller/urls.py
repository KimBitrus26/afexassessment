
from django.urls import path

from .views import *

urlpatterns = [
    path('dashboard', index, name="home"),
    path('', login, name='login'),
    path('logout/', logout, name='logout'),
    path('signup/', signup, name='signup'),
    path('search/', search_users, name='search'),
    path('profile/', profile_view, name='profile'),
    path('edit-profile/', add_profile_photo, name='edit-profile'),
    path('add-friend/<int:user_id>/', add_friend, name='add-friend'),
    path('friend-request/', friend_request_view, name='friend-request'),
    path('friend-request-accept/<int:friend_request_id>/', accept_friend_request, name='friend-request-accept'),
    path('friend-request-reject/<int:friend_request_id>/', reject_friend_request, name='friend-request-reject'),
    path('friends/', friends_view, name='friends'),

    ]
