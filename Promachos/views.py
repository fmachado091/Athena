# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf
from Cerberus.forms import UserRegistrationForm
from django.template import RequestContext
from django.shortcuts import render, render_to_response
from .forms import UploadFileForm, TurmaCreationForm, AtividadeCreationForm
from Aeacus import compare
from Athena.models import Professor, Turma, Atividade, Aluno
from pprint import pprint
import re
import logging

logr = logging.getLogger(__name__)


def login(request):

    if request.user.is_authenticated():

        professor = Professor.objects.filter(user=request.user)
        aluno = Aluno.objects.filter(user=request.user)

        if aluno:
            return HttpResponseRedirect('/aluno')

        if professor:
            return HttpResponseRedirect('/professor')

    if request.method == 'POST':

        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)

            matchObjAluno = re.match(
                r'(.*)@aluno.ita.br$', user.email, re.M | re.I)

            if matchObjAluno:
                return HttpResponseRedirect('/aluno')
            return HttpResponseRedirect('/professor')

        else:
            return render_to_response(
                'login.html',
                {"invalid_message": "Login inválido. Tente novamente."},
                context_instance=RequestContext(request),
            )

    return render_to_response('login.html',
                              {"invalid_message": ""},
                              context_instance=RequestContext(request))


def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return render_to_response(
                'cadastro.html',
                {"success_message": "O cadastro foi realizado com sucesso!"},
                context_instance=RequestContext(request),
            )

    else:
        form = UserRegistrationForm()
    args = {}
    args.update(csrf(request))

    args['form'] = form

    return render_to_response('cadastro.html', args)


def home(request):

    if request.user.is_authenticated():
        form = UploadFileForm()
        if request.method == 'POST':
            entrada = request.FILES.getlist('file')[0]
            saida = request.FILES.getlist('file')[1]
            fonte = request.FILES.getlist('file')[2]

            resultado = compare.mover(entrada, saida, fonte)

            return render(
                request, 'teste_juiz.html',
                {
                    'form': form,
                    'resultado': resultado,
                }
            )

        return render(request, 'teste_juiz.html', {'form': form})

    else:
        return HttpResponseRedirect('/login')


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/login')


def professor(request):

    professor = Professor.objects.filter(user=request.user)
    if request.user.is_authenticated() is False or not professor:
        return HttpResponseRedirect('/login')
    professor = professor[0]

    form = TurmaCreationForm()
    if request.method == 'POST':
        pprint(request.POST)
        if('post_turma' in request.POST):
            turma = Turma(
                nome=request.POST['nome'],
                descricao=request.POST['descricao'],
                professor=professor,
            )
            turma.save()
        elif ('post_atividade' in request.POST):
            turma = Turma.objects.get(id=request.POST['id_turma'])
            atividade = Atividade(
                nome=request.POST['nome'],
                descricao=request.POST['descricao'],
                data_limite=request.POST['data_limite'],
                arquivo_roteiro=request.FILES['arquivo_roteiro'],
                arquivo_entrada=request.FILES['arquivo_entrada'],
                arquivo_saida=request.FILES['arquivo_saida'],
                turma=turma,
            )
            atividade.save()
        elif ('post_deletar' in request.POST):
            turma = Turma.objects.get(id=request.POST['id_turma'])
            turma.delete()

    turmas = Turma.objects.filter(professor=professor)
    panes = []
    for turma in turmas:
        atividades = Atividade.objects.filter(turma=turma)
        panes.append(
            render_to_response(
                'pane_professor.html',
                {
                    "turma": turma,
                    "atividades": atividades,
                    "form": AtividadeCreationForm(),
                },
                context_instance=RequestContext(request),
            ).content
        )

    return render_to_response(
        'professor.html',
        {"turmas": turmas,
         "panes": panes,
         "form": form},
        context_instance=RequestContext(request),
    )


def prof_ativ(request):
    professor = Professor.objects.filter(user=request.user)
    if request.user.is_authenticated() is False or not professor:
        return HttpResponseRedirect('/login')
    return render_to_response('prof_ativ.html')


def aluno(request):
    aluno = Aluno.objects.filter(user=request.user)
    if request.user.is_authenticated() is False or not aluno:
        return HttpResponseRedirect('/login')
    aluno = aluno[0]

    turmas = aluno.turma_set.all()
    """panes = []
    for turma in turmas:
        atividades = Atividade.objects.filter(turma=turma)
        panes.append(
            render_to_response(
                'pane_professor.html',
                {
                    "turma": turma,
                    "atividades": atividades,
                    "form": AtividadeCreationForm(),
                },
                context_instance=RequestContext(request),
            ).content
        )
    """
    return render_to_response(
        'aluno.html',
        {"turmas": turmas},
        context_instance=RequestContext(request),
    )


def aluno_ativ(request):
    aluno = Aluno.objects.filter(user=request.user)
    if request.user.is_authenticated() is False or not aluno:
        return HttpResponseRedirect('/login')
    return render_to_response('ativ_exemplo.html')


def aluno_turmas(request):
    aluno = Aluno.objects.filter(user=request.user)
    if request.user.is_authenticated() is False or not aluno:
        return HttpResponseRedirect('/login')
    aluno = aluno[0]

    if request.method == 'POST':
        pprint(request.POST)
        if('post_sair' in request.POST):
            turma = Turma.objects.get(id=request.POST['post_sair'])
            aluno.turma_set.remove(turma)
            aluno.save()
        if('post_entrar' in request.POST):
            turma = Turma.objects.get(id=request.POST['post_entrar'])
            aluno.turma_set.add(turma)
            aluno.save()

    turmas_registradas = aluno.turma_set.all()
    todas_turmas = Turma.objects.all()
    turmas_nao_registradas = todas_turmas.exclude(
        id__in=[turma_check.id for turma_check in turmas_registradas]
    )

    return render_to_response(
        'lista_turmas.html',
        {
            "turmas_registradas": turmas_registradas,
            "turmas_nao_registradas": turmas_nao_registradas,
        },
        context_instance=RequestContext(request),
    )
