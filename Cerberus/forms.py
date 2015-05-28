# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import re


class MyRegistrationForm(UserCreationForm):
    travis1 = "Esse valor deve contar apenas letras"
    travis2 = ", números e os caracteres @/./+/-/_."
    username = forms.RegexField(
        label=("Usuário"),
        max_length=30,
        regex=r'^[\w.@+-]+$',
        help_text =
        ("<br>No máximo 30 caracteres. Letras, dígitos e @/./+/-/_ apenas."),
        error_messages = {'Inválido': (travis1 + travis2)}
    )

    password1 = forms.CharField(
        label=("Senha"),
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label=("Confirme a sua senha"),
        widget=forms.PasswordInput,
        help_text = ("<br>Insira a mesma senha para verificação.")
    )

    email = forms.EmailField(
        label=("Email"),
        required=True
    )

    def clean_email(self):
        data = self.cleaned_data['email']

        matchObjProf = re.match(r'(.*)@ita.br$', data, re.M | re.I)
        matchObjAluno = re.match(r'(.*)@aluno.ita.br$', data, re.M | re.I)
        matchObjAdmin = re.match(r'(.*)@admin.ita.br$', data, re.M | re.I)

        if (
            not matchObjProf and not
            matchObjAluno and not
            matchObjAdmin
        ):
            raise forms.ValidationError(
                "O email deve ser do formato @ita.br ou @aluno.ita.br."
            )
        return data

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(MyRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        # user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()
        return user


class ContactForm1(forms.Form):
    subject = forms.CharField(max_length=100)


class ContactForm2(forms.Form):
    sender = forms.EmailField()


class ContactForm3(forms.Form):
    message = forms.CharField(widget=forms.Textarea)
