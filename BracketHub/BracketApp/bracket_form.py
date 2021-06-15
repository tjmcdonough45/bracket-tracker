from django import forms
from django.forms.models import inlineformset_factory
from django.core import validators
from BracketApp.models import Show,Season,Player,Contestant,Bracket,Score,Bonus


class PlayerForm(forms.ModelForm):
    #Define fields here if want to do custom validators
    class Meta():
        model = Player
        fields = ('name',)
        help_texts = {
            'name': "The alias under which you'd like to submit your bracket. It can be the same as your username...or not! Go wild!"
        }
        # widgets = {
        #     'user': forms.TextInput(attrs={'readonly': 'readonly'}), #make user field read-only; set to current user in view
        #     'season': forms.TextInput(attrs={'readonly': 'readonly'}), #make season field read-only; set to current season in view
        # }

# class BracketInput(forms.ModelForm):
#     class Meta():
#         model = Bracket
#         exclude = ('player',)

class BaseBracketFormSet(forms.BaseInlineFormSet):
    def __init__(self, season, *args, **kwargs):
        super(BaseBracketFormSet, self).__init__(*args, **kwargs)
        for form in self:
            form.fields['contestant'].queryset = Contestant.objects.filter(season__exact=season,actual_elimination__gte=season.first_scored_elimination).order_by('first_name')

    def clean(self):
        """Checks that no two brackets have the same contestant."""
        if any(self.errors):
            # Don't bother validating the formset unless each form is valid on its own
            return
        contestants = []
        for form in self.forms:
            contestant = form.cleaned_data['contestant']
            if contestant in contestants:
                raise forms.ValidationError("Select each contestant only once.")
            contestants.append(contestant)

BracketFormSet = inlineformset_factory(Player, #parent form
                                        Bracket, #inline form model
                                        formset=BaseBracketFormSet,
                                        fields=['predicted_elimination','contestant'], #inline form fields
                                        #fields=['predicted_rank','contestant'], #inline form fields
                                        # fields=['contestant'],
                                        labels={ #labels for the fields
                                            'contestant':'Contestant',
                                            'predicted_elimination':'Rose Ceremony',
                                            #'predicted_rank':'Finish',
                                        },
                                        help_texts={ #help texts for the fields
                                            'contestant': None,
                                            'predicted_elimination': None,
                                            #'predicted_rank': None,
                                        },
                                        widgets = {
                                            'predicted_elimination': forms.TextInput(attrs={'readonly': 'readonly'}), #make predicted_elimination field read-only; populate with necessary options in view
                                            #'predicted_rank': forms.TextInput(attrs={'readonly': 'readonly'}), #make predicted_rank field read-only; populate with necessary options in view
                                        },
                                        can_delete=False, #set to false because can't delete a non-existent instance
                                        extra=23) #how many inline forms are in template by default

class BonusForm(forms.ModelForm):
    class Meta():
        model = Bonus
        fields = ('most_confessionals','most_individual_immunity_wins','most_votes_against',)

    def __init__(self, season, *args, **kwargs):
        super(BonusForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].queryset = Contestant.objects.filter(season__exact=season,actual_elimination__gte=season.first_scored_elimination).order_by('first_name')

# Add custom validator (as below) by inserting validators=[function_name] into Field argument
# def check_for_z(value):
#     if value[0].lower() != 'z':
#         raise forms.ValidationError('NAME NEEDS TO START WITH Z')

# class BracketInput(forms.Form):
#     name = forms.CharField(max_length=69)
#     email = forms.EmailField()
#     verify_email = forms.EmailField(label='Enter your email again:')
#     botcatcher = forms.CharField(required=False,
#                                 widget=forms.HiddenInput,
#                                 validators=[validators.MaxLengthValidator(0)])

    # To clean entire form at once:
    # def clean(self):
    #     all_clean_data = super().clean()
    #     email = all_clean_data['email']
    #     vmail = all_clean_data['verify_email']
    #
    #     if email != vmail:
    #         raise forms.ValidationError('MAKE SURE EMAILS MATCH!')

    # To clean one particular part of form:
    # def clean_botcatcher(self):
    #     botcatcher = self.cleaned_data['botcatcher']
    #     if len(botcatcher) > 0:
    #         raise forms.ValidationError('GOTCHA BOT!')
    #     return botcatcher
