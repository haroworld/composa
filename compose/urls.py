from unicodedata import name
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="home"),

    path('comment/<str:pk>/', views.commentPost, name="comment"),
    path('uncomment/<str:pk>/', views.unComment, name="uncomment"),

    path('deletepost/', views.DeletePost, name="deletepost"),
    path('repost/<str:pk>/', views.Repost, name="repost"),
    path('delete-repost/<str:pk>/', views.UndoRepost, name="delete-repost"),
    path('likepost/', views.LikePost, name="likepost"),
    path('unlike/<str:pk>/', views.UnlikPost, name="unlike"),

    path('single_post/<str:pk>/', views.singlePost, name="single_post"),
    
]