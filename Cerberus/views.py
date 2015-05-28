from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf
from forms import MyRegistrationForm
from django.core.mail import send_mail

import logging

logr = logging.getLogger(__name__)


def login(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('login.html', c)


def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/aluno')
    else:
        return HttpResponseRedirect('/invalido')


def loggedin(request):
    return render_to_response('aluno.html',
                              {'full_name': request.user.username})


def invalid_login(request):
    return render_to_response('login_invalido.html')


def logout(request):
    auth.logout(request)
    return render_to_response('logout.html')


def register_user(request):
    if request.method == 'POST':
        form = MyRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/registro_sucesso')

    else:
        form = MyRegistrationForm()
    args = {}
    args.update(csrf(request))

    args['form'] = form

    return render_to_response('cadastro.html', args)


def register_success(request):
    return render_to_response('registro_sucesso.html')


def process_form_data(form_list):
    form_data = [form.cleaned_data for form in form_list]

    logr.debug(form_data[0]['subject'])
    logr.debug(form_data[1]['sender'])
    logr.debug(form_data[2]['message'])

    send_mail(form_data[0]['subject'],
              form_data[2]['message'], form_data[1]['sender'],
              ['hibbert.michael@gmail.com'], fail_silently=False)

    return form_data

# Create your views here.
