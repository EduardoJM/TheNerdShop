from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm as OriginalUserCreationForm
from django import forms

from ..models.user import User

class UserCreationForm(OriginalUserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']

class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = [
            'cpf', 'phone_code', 'phone_number', 'first_name',
            'last_name', 'billing_address_street', 'billing_address_number',
            'billing_address_complement', 'billing_address_district',
            'billing_address_postal_code', 'billing_address_city',
            'billing_address_state', 'billing_address_country'
        ]
