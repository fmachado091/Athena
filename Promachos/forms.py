from django import forms
from django.forms import ModelForm
from Athena.models import Turma, Atividade


class UploadFileForm(forms.Form):

    file = forms.FileField()


class TurmaCreationForm(ModelForm):
    class Meta:
        model = Turma
        fields = ['nome', 'descricao']


class AtividadeCreationForm(ModelForm):
    class Meta:
        model = Atividade
        fields = ['nome', 'descricao', 'arquivo_roteiro', 'arquivo_entrada',
            'arquivo_saida', 'data_limite']
