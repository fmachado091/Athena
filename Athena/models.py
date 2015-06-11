from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Aluno(models.Model):

    nome = models.CharField(max_length=50, help_text="Nome do Aluno")
    usuario = models.ForeignKey(
        User,
        help_text="Usuario de login relacionado ao Aluno",
    )


class Professor(models.Model):

    nome = models.CharField(max_length=50, help_text="Nome do Professor")
    usuario = models.ForeignKey(
        User,
        help_text="Usuario de login relacionado ao Professor",
    )


class Turma(models.Model):

    nome = models.CharField(max_length=50, help_text="Nome da Turma")
    descricao = models.CharField(max_length=2000, help_text="Texto da Turma")
    dono = models.ForeignKey(Professor, help_text="Professor dono a Turma")
    alunos = models.ManyToManyField(
        Aluno,
        help_text="Alunos inscritos na turma",
    )


class Atividade(models.Model):

    def _atividade_path(instance, filename):
        return 'atividades/{0}/{1}'.format(instance.id, filename)

    def estaFechada(self):
        return self.data_limite <= timezone.now()

    nome = models.CharField(max_length=50, help_text="Nome da atividade")
    descricao = models.CharField(
        max_length=1000,
        help_text="Breve descricao da Atividade",
    )
    arquivo_roteiro = models.FileField(upload_to=_atividade_path)
    arquivo_entrada = models.FileField(upload_to=_atividade_path)
    arquivo_saida = models.FileField(upload_to=_atividade_path)
    data_limite = models.DateField(help_text="Data limite para a entrega")
    turma = models.ForeignKey(
        Turma,
        help_text="Turma a qual a atividade pertence",
    )
    alunos = models.ManyToManyField(
        Aluno,
        through='RelAlunoAtividade',
        help_text="""Relacao do aluno com a atividade,
            guarda se aluno submeteu atividade""",
    )


class Submissao(models.Model):

    def _atividade_path(instance, filename):
        return 'codigos/{0}/{1}/{2}'.format(
            instance.aluno.id,
            instance.atividade.id,
            filename,
        )

    RESULTADOS = (
        ('AC', 'Aceito'),
        ('TLE', 'Tempo Limite Excedido'),
        ('RTE', 'Erro em tempo de execucao'),
        ('CE', 'Erro de compilacao'),
        ('WA', 'Resposta Errada'),
    )
    data_envio = models.DateField(
        auto_now=True,
        help_text='Data de submissao do codigo',
    )
    # arquivo codigo
    resultado = models.CharField(
        max_length=3,
        choices=RESULTADOS,
        help_text='Resultado da submissao do aluno',
    )
    nota = models.PositiveSmallIntegerField(
        help_text='Nota para submissao do aluno'
    )
    atividade = models.ForeignKey(
        Atividade,
        help_text="Atividade relacionada a submissao"
    )
    aluno = models.ForeignKey(Aluno, help_text="Aluno que enviou a submissao")


class RelAlunoAtividade(models.Model):

    foiEntregue = models.BooleanField(
        help_text='Se o aluno ja mandou alguma submissao para a atividade'
    )
    aluno = models.ForeignKey(Aluno, help_text="Aluno inscrito na atividade")
    atividade = models.ForeignKey(Atividade, help_text="Atividade do aluno")
