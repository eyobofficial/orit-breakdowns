from django import forms
from django.contrib.auth.forms import UserCreationForm

class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=60)
    last_name = forms.CharField(max_length=60)

class StepOneForm(forms.Form):
    OPTION_CHOICES = (
            ('0', 'Select a cost breakdown form the standard library to edit'),
            ('1', 'Create a new cost breakdown form scratch'),
        )
    options = forms.ChoiceField(widget=forms.RadioSelect, choices=OPTION_CHOICES, initial='0')

    BREAKDOWN_CHOICES = (
            (None, '---------'),
            ('1', 'breakdown 1'),
            ('2', 'breakdown 2'),
        )
    breakdown = forms.TypedChoiceField(choices=BREAKDOWN_CHOICES, coerce=int, required=False)

    def clean(self):
        super(StepOneForm, self).clean()
        options = self.cleaned_data.get('options')
        breakdown = self.cleaned_data.get('breakdown')

        if int(options) == 0 and breakdown is None:
            # self.add_error('breakdown', 'Please select a breakdown')
            raise forms.ValidationError('select shit')
        # return self.cleaned_data