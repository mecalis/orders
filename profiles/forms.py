from django import forms
from django.contrib.auth.models import User
from .models import Profile

from django.contrib.auth.forms import UserCreationForm

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model= User
        fields = ['username', 'email', 'password']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', 'email_confirmed', 'last_post_id')

class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=254, label='Felhasználó név:')
    email = forms.EmailField(max_length=254, help_text='Szükséges. Valós e-mail címet adj meg!', label='E-mail cím:')
    password1 = forms.CharField(widget=forms.PasswordInput, label='Jelszó:')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Jelszó ellenőrzése:')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )