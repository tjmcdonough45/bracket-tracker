from django.urls import path
from BracketApp import views

#TEMPLATE TAGGING
app_name = 'BracketApp'

urlpatterns = [
    path('form/',views.bracket_input_view,name='bracket_input'),
    path('brackets/', views.brackets, name='brackets'),
    path('help/', views.help, name='help'),
]
