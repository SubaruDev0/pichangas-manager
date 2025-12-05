from django.urls import path
from . import views

urlpatterns = [
    path('', views.match_list, name='match_list'),
    path('match/create/', views.create_match, name='create_match'),
    path('match/<int:match_id>/', views.match_detail, name='match_detail'),
    path('match/<int:match_id>/join/', views.toggle_attendance, name='toggle_attendance'),
    path('match/<int:match_id>/paid/<int:attendance_id>/', views.mark_paid, name='mark_paid'),
    path('match/<int:match_id>/shuffle/', views.shuffle_teams, name='shuffle_teams'),
    path('match/<int:match_id>/reset-teams/', views.reset_teams, name='reset_teams'),
    path('match/<int:match_id>/delete/', views.delete_match, name='delete_match'),
    path('match/<int:match_id>/remove/<int:attendance_id>/', views.remove_player, name='remove_player'),
]
