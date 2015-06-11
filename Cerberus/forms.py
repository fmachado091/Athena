# -*- coding: utf-8 -*-
from pprint import pprint
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from Athena.models import Professor
import re


class MyRegistrationForm(UserCreationForm):
    travis1 = "Esse valor deve conter apenas letras"
    travis2 = ", números e os caracteres @/./+/-/_."

    password_error_messages = {
        'password_mismatch': ("As senhas inseridas não são compatíveis."),
    }

    fullname = forms.CharField(
        label=("Nome completo"),
        max_length=50,
        error_messages = {
            'required': ("Este campo é obrigatório."),
            'unique': ("Um usuário já possui um cadastro com esse nome."),
        }
    )

    username = forms.RegexField(
        label=("Usuário"),
        max_length=30,
        regex=r'^[\w.@+-]+$',
        help_text =
        ("<br>No máximo 30 caracteres. Letras, dígitos e @/./+/-/_ apenas."),
        error_messages = {
            'invalid': (travis1 + travis2),
            'required': ("Este campo é obrigatório."),
            'unique': ("Um usuário já possui um cadastro com esse nome."),
        }
    )

    password1 = forms.CharField(
        label=("Senha"),
        widget=forms.PasswordInput,
        error_messages = {
            'required': ("Este campo é obrigatório."),
        }
    )

    password2 = forms.CharField(
        label=("Confirme a sua senha"),
        widget=forms.PasswordInput,
        help_text = ("<br>Insira a mesma senha para verificação."),
        error_messages = {
            'required': ("Este campo é obrigatório."),
        }
    )

    email = forms.EmailField(
        required=True,
        error_messages={
            'invalid': (
                "O email deve ser do domínio @ita.br ou @aluno.ita.br"
            ),
            'required': ("Este campo é obrigatório."),
            'unique': ("Um usuário já possui um cadastro com esse email."),
        }
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')

        matchObjProf = re.match(r'(.*)@ita.br$', email, re.M | re.I)
        matchObjAluno = re.match(r'(.*)@aluno.ita.br$', email, re.M | re.I)

        if (
            not matchObjProf and not
            matchObjAluno
        ):
            raise forms.ValidationError(
                "O email deve ser do domínio @ita.br ou @aluno.ita.br"
            )

        if (
            User.objects.filter(email=email).exclude(username=username).count()
        ):
            raise forms.ValidationError(
                "Um usuário já possui um cadastro com esse email."
            )
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.password_error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    class Meta:
        model = User
        fields = ('fullname', 'username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        usuario = super(MyRegistrationForm, self).save(commit=False)
        usuario.email = self.cleaned_data['email']
        pprint(self.fields['fullname'])

        if commit:
            usuario.save()
            professor = Professor(user=usuario, nome=self.fields['fullname'])
            professor.save()

        return usuario
