from django.urls import path
from BracketApp import views

#TEMPLATE TAGGING
app_name = 'BracketApp'

urlpatterns = [
    path('bracket_entry/',views.bracket_entry,name='bracket_entry'),
    path('current_season/', views.current_season, name='current_season'),
    path('past_seasons/', views.past_seasons, name='past_seasons'),
    path('create/',views.PlayerCreateView.as_view(),name='create'),
    path('update/<int:pk>/',views.PlayerUpdateView.as_view(),name='update'),
    path('delete/<int:pk>/',views.PlayerDeleteView.as_view(),name='delete'),
    path('help/', views.help, name='help'),
]
