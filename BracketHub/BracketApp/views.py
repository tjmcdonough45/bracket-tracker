from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from BracketApp.models import UserProfileInfo,Show,Season,Point,Player,Contestant,Bracket,Score,Bonus
from BracketApp.bracket_form import PlayerForm,BracketFormSet
from BracketApp.registration_form import UserForm,UserProfileInfoForm
import numpy as np
from django.views.generic import View,TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy,reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from itertools import chain

# Create your views here.

# Function Based Views (FBVs)
# def index(request):
#     return render(request,'BracketApp/index.html')

def help(request):
    help_dict = {'help':'HELP PAGE'}
    return render(request,'BracketApp/help.html',context=help_dict)

def current_season(request):
    season = Season.objects.filter(current_season__exact=True)
    cur_elimination = season.values()[0]['current_elimination']
    first_scored_elimination = season.values()[0]['first_scored_elimination']
    # cur_elimination = season.current_elimination
    cur_scoring_round = cur_elimination-first_scored_elimination+1
    players = Player.objects.filter(season__current_season__exact=True)
    contestants = Contestant.objects.filter(season__current_season__exact=True)
    num_contestants = len(contestants.values_list())
    points = Point.objects.filter(season__current_season__exact=True).values_list('num_boots',flat=True)
    num_scoring_rounds = len(points)
    num_eliminations = num_scoring_rounds+first_scored_elimination-1
    cur_boots = contestants.filter(actual_elimination__lte=cur_elimination).order_by('actual_rank')
    predicted_rank_init = [1,2,3,4,5,5,6,6,6,7,7,7,8,8,8,9,9,9,10,10,10,10,10]

    cur_scores = Score.objects.filter(elimination__exact=cur_elimination).order_by('rank','-maximum_points_remaining')
    scores = {}
    pics = {}
    brackets_and_pics = {}
    cur_scores_and_pics = {}
    for player in players:
        bracket = Bracket.objects.filter(player__exact=player).order_by('predicted_rank')
        # cur_score = cur_scores.filter(player__exact=player)
        scores[player] = Score.objects.filter(player__exact=player).order_by('elimination')
        pic = player.user.profile_pic
        brackets_and_pics[player] = {'bracket':bracket,'pic':pic}
        # cur_scores_and_pics[player] = {'cur_score':cur_score,'pic':pic}
    # for i in np.arange(num_contestants)+1:
    #     brackets[points[i]] = Bracket.objects.filter(predicted_rank__exact=i).order_by('player__name')
    bonus = contestants.order_by('-num_confessionals','-num_individual_immunity_wins','-num_votes_against')
    bonus_picks = Bonus.objects.all()

    most_confessionals = contestants.order_by('-num_confessionals').first()
    most_individual_immunity_wins = contestants.order_by('-num_individual_immunity_wins').first()
    most_votes_against = contestants.order_by('-num_votes_against').first()

    dict = {'season':season,'players':players,'cur_boots':cur_boots,'bonus':bonus,'cur_scores':cur_scores,
        'scores':scores,'cur_scoring_round':cur_scoring_round,'num_scoring_rounds':num_scoring_rounds,
        'ranks':predicted_rank_init,'bonus_picks':bonus_picks,'most_confessionals':most_confessionals,'most_individual_immunity_wins':most_individual_immunity_wins,
        'most_votes_against':most_votes_against,'brackets_and_pics':brackets_and_pics,'cur_scores_and_pics':cur_scores_and_pics}
    return render(request,'BracketApp/current_season.html',context=dict)

# def past_seasons(request):
#     players = Player.objects.all()
#     shows = Season.objects.order_by('show')
#     seasons = {}
#     for show in shows:
#         seasons[show] = Season.objects.filter(current_season__exact=False,show__name__exact=show).order_by('subtitle')
#     dict = {'players':players,'shows':shows,'seasons':seasons}
#     return render(request,'BracketApp/past_seasons.html',context=dict)

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

def relative(request):
    return render(request,'BracketApp/relative_url_templates.html')

# Class Based Views (CBVs)

# class CBView(View):
#     def get(self,request):
#         return HttpResponse('CBVs are dopeee!')

class IndexView(TemplateView):
    template_name = 'BracketApp/BracketApp_index.html'

    # def get_context_data(self,**kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['injectme'] = 'BASIC INJECTION!'
    #     return context

class SeasonListView(ListView):
    context_object_name = 'seasons'
    model = Season

class SeasonDetailView(DetailView):
    context_object_name = 'season_detail'
    model = Season
    template_name = 'BracketApp/season_detail.html'

class PlayerCreateView(CreateView):
    # fields = ('name',)
    model = Player
    template_name = 'BracketApp/bracket_form.html'
    form_class = PlayerForm
    object = None

    def get(self,request,*args,**kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        bracket_form = BracketFormSet()
        return self.render_to_response(self.get_context_data(form=form,bracket_form=bracket_form))

    def post(self,request,*args,**kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        bracket_form = BracketFormSet(self.request.POST)
        if form.is_valid() and bracket_form.is_valid():
            return self.form_valid(form,bracket_form)
        else:
            return self.form_invalid(form,bracket_form)

    def form_valid(self, form, bracket_form):
        """
        Called if all forms are valid. Creates Player instance along with the
        associated Bracket instances then redirects to success url
        Args:
            form: Player Form
            bracket_form: Bracket Form

        Returns: an HttpResponse to success url

        """
        self.object = form.save(commit=False)
        # pre-processing for Player instance here...
        self.object.save()

        # saving Bracket Instances
        contestants = Contestant.objects.filter(season__current_season__exact=True)
        num_eliminations = len(contestants.values_list('last_name',flat=True))-1
        brackets = bracket_form.save(commit=False)
        for br in brackets:
            #  change the Bracket instance values here
            #  br.some_field = some_value
            br.player = self.object
            br.save()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, bracket_form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.

        Args:
            form: Player Form
            bracket_form: Bracket Form
        """
        return self.render_to_response(
                 self.get_context_data(form=form,
                                       bracket_form=bracket_form
                                       )
        )

class UserProfileInfoUpdateView(UpdateView):
    model = UserProfileInfo
    fields = ['profile_pic']
    template_name = 'BracketApp/update_profile_form.html'

    #Need this function or else update doesn't work beyond pk=1
    def get_object(self,queryset=None):
        return self.request.user.userprofileinfo

    def get_success_url(self):
        return reverse('index')

class PlayerDeleteView(DeleteView):
    model = Player
    success_url = reverse_lazy('BracketApp:seasons')

@login_required
def special(request):
    # Remember to also set login url in settings.py!
    # LOGIN_URL = '/BracketApp/user_login/'
    return HttpResponse("You are logged in. Nice!")

@login_required
def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return HttpResponseRedirect(reverse('index'))

def register(request):

    registered = False

    if request.method == 'POST':

        # Get info from "both" forms
        # It appears as one form to the user on the .html page
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        # Check to see both forms are valid
        if user_form.is_valid() and profile_form.is_valid():

            # Save User Form to Database
            user = user_form.save()

            raw_password = user_form.cleaned_data.get('password1')

            # Hash the password
            user.set_password(raw_password)

            # Update with Hashed password
            user.save()

            # Now we deal with the extra info!

            # Can't commit yet because we still need to manipulate
            profile = profile_form.save(commit=False)

            # Set One to One relationship between
            # UserForm and UserProfileInfoForm
            profile.user = user

            # Check if they provided a profile picture
            if 'profile_pic' in request.FILES:
                print('found it')
                # If yes, then grab it from the POST form reply
                profile.profile_pic = request.FILES['profile_pic']

            # Now save model
            profile.save()

            # Registration Successful!
            registered = True

        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors,profile_form.errors)

    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    # This is the render and context dictionary to feed
    # back to the registration.html file page.
    return render(request,'BracketApp/registration_form.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})

def user_login(request):

    if request.method == 'POST':
        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)

        # If we have a user
        if user:
            #Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request,user)
                # Send the user back to some page.
                # In this case their homepage.
                return HttpResponseRedirect(reverse('index'))
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        #Nothing has been provided for username or password.
        return render(request, 'BracketApp/login_form.html', {})

def bracket_entry(request):
    user = request.user
    userprofileinfo = UserProfileInfo.objects.filter(user__exact=user)[0]
    season = Season.objects.filter(current_season__exact=True)
    first_scored_elimination = season.values()[0]['first_scored_elimination']
    points = Point.objects.filter(season__current_season__exact=True)
    num_scoring_rounds = len(points.values_list())
    num_eliminations = num_scoring_rounds+first_scored_elimination-1
    contestants = Contestant.objects.filter(season__current_season__exact=True,actual_elimination__exact=69)
    num_contestants = len(contestants.values_list())
    predicted_rank_init = [1,2,3,4,5,5,6,6,6,7,7,7,8,8,8,9,9,9,10,10,10,10,10]

    if len(Bracket.objects.filter(player__user__exact=userprofileinfo,player__season__exact=season[0]).values_list())==0:
        submitted = False
        if request.method == "POST":
            player_form = PlayerForm(data=request.POST)
            bracket_form = BracketFormSet(data=request.POST)
            if player_form.is_valid() and bracket_form.is_valid():
                new_player = player_form.save(commit=False)
                new_player.user = userprofileinfo
                new_player.season = season[0]
                new_player.save()
                new_bracket = bracket_form.save(commit=False)
                for br in new_bracket:
                    br.player = new_player
                    # br.predicted_rank = 1
                    br.predicted_elimination = num_eliminations-br.predicted_rank+2
                    # br.contestant = contestants[0]
                    br.save()
                    submitted=True
                # new_bracket.save()
            else:
                # One of the forms was invalid if this else gets called.
                print(player_form.errors,bracket_form.errors)
        else:
            player_form = PlayerForm()
            bracket_form = BracketFormSet(initial=[{'contestant':j,
                                                    'predicted_rank': predicted_rank_init[i]
                                                    } for i,j in zip(np.arange(num_contestants),contestants)])
    else:
        submitted = True
        player_form = PlayerForm()
        bracket_form = BracketFormSet(initial=[{'contestant':j,
                                                'predicted_rank': predicted_rank_init[i]
                                                } for i,j in zip(np.arange(num_contestants),contestants)])
    return render(request,'BracketApp/bracket_form.html',{'player_form':player_form,'bracket_form':bracket_form,'submitted':submitted})
