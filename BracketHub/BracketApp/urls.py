from django.urls import path
from BracketApp import views

#TEMPLATE TAGGING
app_name = 'BracketApp'

urlpatterns = [
    path('bracket_entry/',views.bracket_entry,name='bracket_entry'),
    path('current_season/', views.current_season, name='current_season'),
    path('help/', views.help, name='help'),
]
