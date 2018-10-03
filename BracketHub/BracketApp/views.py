from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from BracketApp.models import Show,Season,Player,Contestant,Bracket,Score
from BracketApp import form
from BracketApp.form import PlayerInput,BracketInput

num_eliminations=2 #eventually have this set from the value in current_season

# Create your views here.
def index(request):
    return render(request,'BracketApp/index.html')

def help(request):
    help_dict = {'help':'HELP PAGE'}
    return render(request,'BracketApp/help.html',context=help_dict)

def brackets(request):
    player_list = Player.objects.order_by('name')
    # bracket_list = Bracket.objects.order_by('player','predicted_elimination')
    bracket_dict = {}
    score_dict = {}
    for player in player_list:
        bracket_dict[player] = Bracket.objects.filter(player__exact=player).order_by('predicted_elimination')
        score_dict[player] = Score.objects.filter(player__exact=player).order_by('elimination')
    result_list = Contestant.objects.filter(actual_elimination__lte=num_eliminations).order_by('actual_elimination')
    bonus_list = Contestant.objects.order_by('-num_confessionals','-num_individual_immunity_wins','-num_votes_against')
    cur_score_list = Score.objects.filter(elimination__exact=num_eliminations).order_by('rank')
    # score_list = Score.objects.order_by('elimination','score')
    dict = {'players':player_list,'brackets':bracket_dict,'results':result_list,'bonus':bonus_list,'scores':score_dict,'cur_scores':cur_score_list}
    return render(request,'BracketApp/brackets.html',context=dict)

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

def bracket_input_view(request):
    player_form = PlayerInput(prefix='player')
    bracket_form = BracketInput(prefix='bracket')
    if request.method == "POST":
        player_form = PlayerInput(request.POST,prefix='player')
        bracket_form = BracketInput(request.POST,prefix='bracket')
        if player_form.is_valid() and bracket_form.is_valid():
            new_bracket = bracket_form.save(commit=False)
            new_bracket.player = player_form.save()
            new_bracket = bf.save()
            return index(request)
        else:
            print('FAILED')
    return render(request,'BracketApp/form.html',{'player_form':player_form,'bracket_form':bracket_form})

def relative(request):
    return render(request,'BracketApp/relative_url_templates.html')
