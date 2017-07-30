from django import forms
from django.contrib.auth.forms import UserCreationForm

class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=60)
    last_name = forms.CharField(max_length=60)