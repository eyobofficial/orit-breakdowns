from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CostBreakdown, Project, StandardLibrary

class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=60)
    last_name = forms.CharField(max_length=60)
    email = forms.EmailField(max_length=60)

class StepOneForm(forms.Form):
    OPTION_CHOICES = (
            ('0', 'as'),
            ('1', 'Create a new cost breakdown form scratch'),
        )
    options = forms.ChoiceField(widget=forms.RadioSelect, choices=OPTION_CHOICES)  

class StepTwoForm(forms.ModelForm):
    class Meta:
        model = CostBreakdown
        fields = ['activity_catagory', 'project', 'full_title', 'description', 'unit', 'output', 'overhead', 'profit',]

    def clean_project(self):
        data = self.cleaned_data.get('project')
        if data is None:
            raise forms.ValidationError('This field is required.')

        return data

class ChooseLibraryForm(forms.Form):
    breakdown_library = forms.ModelChoiceField(queryset=StandardLibrary.objects.all())

class CreateBreakdownForm(forms.ModelForm):
    class Meta:
        model = CostBreakdown
        fields = ['project', 'activity_catagory' ,'full_title', 'description', 'unit', 'output', 'overhead', 'profit',]