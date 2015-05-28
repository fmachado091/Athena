from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import re


class MyRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

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
                "Must be a @ita.br or @aluno.ita.br address"
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
