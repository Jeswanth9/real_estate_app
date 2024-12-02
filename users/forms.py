from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'is_owner', 'phone_number']
        help_texts = {
            'username': 'Required. 150 characters or fewer.',
            'email': 'Required. Inform a valid email address.',
            'is_owner': 'Check if you are an owner.',
            'phone_number': 'Enter your phone number.'
        }
        labels = {
            'username': 'Username',
            'email': 'Email',
            'password1': 'Password',
            'password2': 'Confirm Password',
            'is_owner': 'Owner Status',
            'phone_number': 'Phone Number'
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'profile_image']
        help_texts = {
            'username': 'Required. 150 characters or fewer.',
            'email': 'Required. Inform a valid email address.',
            'phone_number': 'Enter your phone number.',
            'profile_image': 'Upload your profile image.'
        }
        labels = {
            'username': 'Username',
            'email': 'Email',
            'phone_number': 'Phone Number',
            'profile_image': 'Profile Image'
        }