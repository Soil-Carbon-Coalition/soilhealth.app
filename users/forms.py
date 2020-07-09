from django import forms
from .models import CustomUser


class SignupForm(forms.Form):
    '''
    this is the only way to add fields that save to
    allauth signup form, and needs pointer in settings.py:
    ACCOUNT_SIGNUP_FORM_CLASS = 'users.forms.SignupForm'
    '''
    full_name = forms.CharField(max_length=60, label='Your full name', required=True,
                                help_text='Your full name, not your email, will be your display name')
    user_location = forms.CharField(
        max_length=60, label='Your location', required=True, help_text='such as town, county, state, country')

    def signup(self, request, user):
        user.full_name = self.cleaned_data['full_name']
        user.user_location = self.cleaned_data['user_location']
        user.save()    # def signup(self, request, user):
