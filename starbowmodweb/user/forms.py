from django import forms
from django.contrib import auth


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = auth.get_user_model()
        fields = ['username', 'email']
