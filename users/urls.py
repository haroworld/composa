from django import views
from django.urls import path
from . import views

urlpatterns = [
    path('login', views.Login, name="login"),
    path('logout', views.Logout, name="logout"),
    path('register', views.Register, name="register"),

    path('profile/', views.Myprofile, name="profile" ),
    path('edit-profile/', views.EditProfile, name="edit-profile"),
    path('delete-account/', views.DeleteAccount, name="delete-account"),

    path('user-account/<str:pk>/', views.UserAccount, name="user-account"),

    path('friend-request/<str:pk>/', views.SendRequest, name="friend-request"),
    path('unfriend/<str:pk>/', views.Unfriend, name="unfriend"),
    path('block_user/<str:pk>/',views.BlockUser, name="block_user"),
    path('unblock_user/<str:pk>/',views.UnBlockUser, name="unblock_user"),

    path('cancle-request/<str:pk>/', views.CancleRequest, name="cancle-request"),
    path('accept-request/<str:pk>/', views.AcceptRequest, name="accept-request"),
    path('delete-request/<str:pk>/', views.DeleteRequest, name="delete-request"),

    path('message/<str:pk>/', views.Messages, name="message"),

    path('userslist', views.AllUsers, name="userslist"),

    path('request_receive/',views.Received_request,name="request_receive"),
    path('request_sent/',views.Sent_request,name="request_sent"),
    path('suggested_user/',views.Suggested_user,name="suggested_user"),

    path('friends/', views.Friends, name="friends"),
    path('account_friends/<str:pk>/', views.AccountFriends, name="account_friends")
]