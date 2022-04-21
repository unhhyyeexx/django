from django.urls import path
from . import views


urlpatterns = [
    path('artists/', views.artists_list),
    path('artists/<int:artists_pk>/', views.artists_detail),
    path('artists/<int:artists_pk>/music/', views.music_create),
    path('music/', views.music_list),
    path('music/<int:music_pk>/', views.music_detail),
]
