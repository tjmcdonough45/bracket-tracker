from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from BracketApp.models import Show,Season,Player,Contestant,Bracket,Score
from BracketApp import form
from BracketApp.form import PlayerInput,BracketInput
import numpy as np

cur_elimination=1 #eventually have this set from the value in current_season

# Create your views here.
def index(request):
    return render(request,'BracketApp/index.html')

def help(request):
    help_dict = {'help':'HELP PAGE'}
    return render(request,'BracketApp/help.html',context=help_dict)

def current_season(request):
    season = Season.objects.filter(current_season__exact=True)
    cur_elimination = season.values()[0]['current_elimination']
    players = Player.objects.order_by('name')
    contestants = Contestant.objects.filter(season__current_season__exact=True)
    num_eliminations = len(contestants.values_list('last_name',flat=True))-1
    cur_boots = contestants.filter(actual_elimination__lte=cur_elimination).order_by('actual_rank')
    brackets = {}
    scores = {}
    for player in players:
        # brackets[player] = Bracket.objects.filter(player__exact=player).order_by('predicted_rank')
        scores[player] = Score.objects.filter(player__exact=player).order_by('elimination')
    for i in np.arange(num_eliminations)+1:
        brackets[i] = Bracket.objects.filter(predicted_rank__exact=i).order_by('player__name')
    bonus = contestants.order_by('-num_confessionals','-num_individual_immunity_wins','-num_votes_against')
    cur_scores = Score.objects.filter(elimination__exact=cur_elimination).order_by('rank')
    dict = {'season':season,'players':players,'brackets':brackets,'cur_boots':cur_boots,'bonus':bonus,'scores':scores,'cur_scores':cur_scores}
    return render(request,'BracketApp/current_season.html',context=dict)

# def bracket_input_view(request):
#     form1 = form.BracketInput()
#     if request.method == 'POST':
#         form1 = form.BracketInput(request.POST)
#         if form1.is_valid():
#             #DO SOMETHING CODE
#             print('VALIDATION SUCCESS!')
#             print('NAME: '+form1.cleaned_data['name'])
#     return render(request,'BracketApp/form.html',{'form':form1})

# def bracket_input_view(request):
#     form = BracketInput()
#     if request.method == 'POST':
#         form = BracketInput(request.POST)
#         if form.is_valid():
#             form.save(commit=True)
#             return index(request)
#         else:
#             print('ERROR FORM INVALID')
#     return render(request,'BracketApp/form.html',{'form':form})

def bracket_entry(request):
    player_form = PlayerInput(prefix='player')
    bracket_form = BracketInput(prefix='bracket')
    if request.method == "POST":
        player_form = PlayerInput(request.POST,prefix='player')
        bracket_form = BracketInput(request.POST,prefix='bracket')
        if player_form.is_valid() and bracket_form.is_valid():
            new_bracket = bracket_form.save(commit=False)
            new_bracket.player = player_form.save()
            new_bracket = bracket_form.save()
            return index(request)
        else:
            print('FAILED')
    return render(request,'BracketApp/form.html',{'player_form':player_form,'bracket_form':bracket_form})

def relative(request):
    return render(request,'BracketApp/relative_url_templates.html')
