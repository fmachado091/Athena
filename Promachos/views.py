# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf
from Cerberus.forms import MyRegistrationForm
from django.template import RequestContext
from django.shortcuts import render, render_to_response
from .forms import UploadFileForm
from Aeacus import compare
import pprint
import re
import logging

logr = logging.getLogger(__name__)


def login(request):

    if request.method == 'POST':

        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)

            matchObjAluno = re.match(
                r'(.*)@aluno.ita.br$', user.email, re.M | re.I)

            if matchObjAluno:
                return HttpResponseRedirect('/home')
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
        form = MyRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return render_to_response(
                'cadastro.html',
                {"success_message": "O cadastro foi realizado com sucesso!"},
                context_instance=RequestContext(request),
            )

    else:
        form = MyRegistrationForm()
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
            pprint.pprint(resultado)
            print(resultado)

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

    if request.user.is_authenticated():
        return render_to_response('professor.html')

    else:
        return HttpResponseRedirect('/login')

def prof_ativ(request):
    return render_to_response('prof_ativ.html')
