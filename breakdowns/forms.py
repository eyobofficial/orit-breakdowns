from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CostBreakdown, Project

class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=60)
    last_name = forms.CharField(max_length=60)
    email = forms.EmailField(max_length=60)

class StepOneForm(forms.Form):
    OPTION_CHOICES = (
            ('0', 'Select a cost breakdown form the standard library to edit'),
            ('1', 'Create a new cost breakdown form scratch'),
        )
    options = forms.ChoiceField(widget=forms.RadioSelect, choices=OPTION_CHOICES, initial='0')  
    breakdown = forms.ModelChoiceField(queryset=CostBreakdown.objects.filter(is_library=True), required=False)

    def clean(self, *args, **kwargs):
        super(StepOneForm, self).clean(*args, **kwargs)
        options = self.cleaned_data.get('options')
        breakdown = self.cleaned_data.get('breakdown')

        if int(options) == 0 and breakdown is None:
            self.add_error('breakdown', 'Please select a breakdown')

class StepTwoForm(forms.ModelForm):
    class Meta:
        model = CostBreakdown
        fields = ['cost_breakdown_catagory', 'project', 'full_title', 'description', 'unit', 'output', 'overhead', 'profit',]

    def clean_project(self):
        data = self.cleaned_data.get('project')
        if data is None:
            raise forms.ValidationError('This field is required.')

        return data