from django.views.generic.base import TemplateView
from Cerberus import views as cerberus_views

class HomeView(TemplateView):

    template_name = "teste_juiz.html"

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

# Create your views here.
