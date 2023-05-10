from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Usuario


class FormHomePage(forms.Form):
    email = forms.EmailField(label=False)


class CriarUsuario(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = Usuario
        fields = ('username', 'email', 'password1','password2')


    