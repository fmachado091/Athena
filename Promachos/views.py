from Cerberus import views as cerberus_views
from django.shortcuts import render
from .forms import UploadFileForm
from Aeacus import compare
import pprint


def home(request):

    form = UploadFileForm()
    if request.method == 'POST':
        entrada = request.FILES.getlist('file')[0]
        saida = request.FILES.getlist('file')[1]
        fonte = request.FILES.getlist('file')[2]

        resultado = compare.mover(entrada, saida, fonte)
        pprint.pprint(resultado)

        return render(
            request, 'teste_juiz.html',
            {
                'form': form,
                'resultado':resultado,
            }
        )

    return render(request, 'teste_juiz.html', {'form': form})


def login_promachos(request):
    return cerberus_views.login(request)


def auth_view_promachos(request):
    return cerberus_views.auth_view(request)


def loggedin_promachos(request):
    return cerberus_views.loggedin(request)


def invalid_login_promachos(request):
    return cerberus_views.invalid_login(request)


def logout_promachos(request):
    return cerberus_views.logout(request)


def register_user_promachos(request):
    return cerberus_views.register_user(request)


def register_success_promachos(request):
    return cerberus_views.register_success(request)
