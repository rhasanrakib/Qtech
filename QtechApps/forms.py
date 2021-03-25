from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

        widgets = {
                'username': forms.TextInput(attrs={'class': 'form-control required', 'Placeholder': 'Input user name'}),
                'first_name': forms.TextInput(attrs={'class': 'form-control required', 'Placeholder': 'Input user name'}),
                'last_name': forms.TextInput(attrs={'class': 'form-control', 'Placeholder': 'Input your last name'}),
                'email': forms.EmailInput(attrs={'class': 'form-control required', 'Placeholder': 'Input your email'}),
                'password1':forms.PasswordInput(attrs={'class': 'form-control required', 'Placeholder': 'Password'}),       
                'password2':forms.PasswordInput(attrs={'class': 'form-control required', 'Placeholder': 'Confirm Password'})       
        }