from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class SignUpForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].error_messages = {
            'unique': 'This email address is already in use.',
            'invalid': 'Enter a valid email address.',
        }

        self.fields['password1'].error_messages = {
            'min_length': 'Password must be at least 8 characters long.',
            'common_password': 'Choose a less common password.',
        }

        self.fields['password2'].error_messages = {
            'min_length': 'Password must be at least 8 characters long.',
            'common_password': 'Choose a less common password.',
            'password_mismatch': 'The passwords do not match.',
        }