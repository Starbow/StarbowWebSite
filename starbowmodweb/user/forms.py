from django import forms
from django.contrib import auth


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = auth.get_user_model()
        fields = ['username', 'email']


class ActivationForm(forms.Form):
    username = forms.CharField(max_length=100)
