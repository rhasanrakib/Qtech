from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    '''
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    '''
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={ 'class': 'form-control form-control-user', 'placeholder': 'Must be 8 Characters'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={ 'class': 'form-control form-control-user', 'placeholder': 'Confirm Password'}))
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

        widgets = {
                'username': forms.TextInput(attrs={'class': 'form-control required', 'Placeholder': 'Input user name'}),
                'first_name': forms.TextInput(attrs={'class': 'form-control', 'Placeholder': 'Input user name'}),
                'last_name': forms.TextInput(attrs={'class': 'form-control', 'Placeholder': 'Input your last name'}),
                'email': forms.EmailInput(attrs={'class': 'form-control required', 'Placeholder': 'Input your email'}),
                
        }