from django.urls import path
from BracketApp import views

#TEMPLATE TAGGING
app_name = 'BracketApp'

urlpatterns = [
    path('bracket_entry/',views.bracket_entry,name='bracket_entry'),
    path('current_season/', views.current_season, name='current_season'),
    path('current_season_survivor/',views.current_season_survivor,name='current_season_survivor'),
    path('seasons/', views.SeasonListView.as_view(), name='seasons'),
    path('seasons/<int:pk>/',views.SeasonDetailView.as_view(),name='detail'),
    path('create/',views.PlayerCreateView.as_view(),name='create'),
    path('update_profile/<int:pk>/',views.UserProfileInfoUpdateView.as_view(),name='update_profile'),
    path('delete/<int:pk>/',views.PlayerDeleteView.as_view(),name='delete'),
    path('register/',views.register,name='register'),
    path('user_login/',views.user_login,name='user_login'),
    path('logout/',views.user_logout,name='logout'),
    path('special/',views.special,name='special'),
    path('help/', views.help, name='help'),
]
