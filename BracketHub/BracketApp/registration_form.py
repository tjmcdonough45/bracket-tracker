from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from BracketApp.models import UserProfileInfo

class UserForm(UserCreationForm):
    #UserCreationForm typically includes username, password1, and password2 fields
    email = forms.EmailField(required=False)

    # this sets the order of the fields
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2",)
        help_texts = {
            'email': 'Optional',
        }

    # this redefines the save function to include the fields you added
    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class UserProfileInfoForm(forms.ModelForm):

    class Meta():
        model = UserProfileInfo
        fields = ('profile_pic',)
        # help_texts = {
        #     'profile_pic': 'Optional',
        # }
