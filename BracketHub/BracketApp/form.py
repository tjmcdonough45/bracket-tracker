from django import forms
from django.forms.models import inlineformset_factory
from django.core import validators
from BracketApp.models import Show,Season,Player,Contestant,Bracket,Score

class PlayerForm(forms.ModelForm):
    #Define fields here if want to do custom validators
    class Meta():
        model = Player
        fields = '__all__'

# class BracketInput(forms.ModelForm):
#     class Meta():
#         model = Bracket
#         exclude = ('player',)

BracketFormSet = inlineformset_factory(Player, #parent form
                                        Bracket, #inline form
                                        fields=['contestant','predicted_elimination'], #inline form fields
                                        labels={ #labels for the fields
                                            'contestant':'Contestant',
                                            'predicted_elimination':'Predicted Elimination',
                                        },
                                        help_texts={ #help texts for the fields
                                            'contestant': None,
                                            'predicted_elimination': None,
                                        },
                                        can_delete=False, #set to false because can't delete a non-existent instance
                                        extra=20) #how many inline forms are in template by default

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
