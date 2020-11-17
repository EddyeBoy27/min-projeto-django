from django import forms
from django.contrib.auth import authenticate

from .models import Aproduto, Acliente


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
    aclinome = forms.CharField(min_length=8, label='Nome')
    aclipass = forms.CharField(
        min_length=6,
        max_length=20,
        widget=forms.TextInput(attrs={'type': 'password'}),
        label='Senha'
    )
    acliemail = forms.EmailField(required=True, label='Email')

    class Meta:
        model = Acliente
        fields = [
            'acliid',
            'aclinome',
            'acliemail',
            'aclipass',
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
        model = Acliente
        fields = [
            'acliemail',
            'aclipass',
        ]
