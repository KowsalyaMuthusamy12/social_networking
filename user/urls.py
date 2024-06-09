from django.urls import path
from user.views import *


urlpatterns=[
    path('signup',SignUP.as_view()),
    path('login',Login.as_view()),
    path('user_search',SearchUsers.as_view()),
    path('friend_request',FriendRequest.as_view()),
    path('accepted_friends',AcceptedFriendsList.as_view()),





]