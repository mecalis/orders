from django import forms
from django.contrib.auth.models import User
from .models import Profile, DailyWaiter
from datetime import datetime

from django.contrib.auth.forms import UserCreationForm

class DailyWaiterForm(forms.Form):
    user = forms.CharField(max_length=64, label='A nap pincérének neve:')
    day = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), initial=datetime.now, label='Amelyik napra vállalom:')

class DailyWaiterModelForm(forms.ModelForm):
    class Meta:
        model = DailyWaiter
        fields = ['user', 'day']

    def clean(self):
        return self.cleaned_data

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model= User
        fields = ['username', 'email', 'password']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', 'email_confirmed', 'last_post_id')
        labels = {
            'bio': 'rövid leírás',
            'avatar': 'avatarod',
            'default_boxes': 'Alapértelmezetten be legyenek-e pipálva a dobozok?',
            # 'content': 'leírás',

        # }
        # help_texts = {
        #     'slug': 'A böngészőben megjelenő url, általában a cím kötőjelekkel elválasztva. Szóközt nem tartalmazhat! pl.: Cím: ma használt cím => Slug: ma-hasznalt-cim',
        }

class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=254, label='Felhasználó név:')
    email = forms.EmailField(max_length=254, help_text='Szükséges. Valós e-mail címet adj meg!', label='E-mail cím:')
    password1 = forms.CharField(widget=forms.PasswordInput, label='Jelszó:')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Jelszó ellenőrzése:')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )