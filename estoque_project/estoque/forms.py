from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from .models import Aproduto


class ProductForm(forms.ModelForm):
    class Meta:
        model = Aproduto
        fields = [
            'aprodnome',
            'aprodvalor',
            'aprodqntd',
            'aprodativo',
        ]


class UserForm(forms.ModelForm):
    username = forms.CharField(min_length=8, label='Nome')
    password = forms.CharField(
        min_length=6,
        max_length=20,
        widget=forms.TextInput(attrs={'type': 'password'}),
        label='Senha'
    )
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
        ]


class LoginForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(LoginForm, self).__init__(*args, **kwargs)

    acliemail = forms.EmailField(required=True, label='Email')
    aclipass = forms.CharField(
        min_length=6,
        max_length=20,
        widget=forms.TextInput(attrs={'type': 'password'}),
        label='Senha'
    )

    class Meta:
        model = User
        fields = [
            'acliemail',
            'aclipass',
        ]
