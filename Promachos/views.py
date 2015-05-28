# from django.shortcuts import render
from django.views.generic.base import TemplateView
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


class LoginView(TemplateView):

    template_name = "login.html"


# Create your views here.
