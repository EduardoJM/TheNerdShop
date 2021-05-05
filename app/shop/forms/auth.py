from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm as OriginalUserCreationForm
from django import forms

from ..models.user import User

class UserCreationForm(OriginalUserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']
