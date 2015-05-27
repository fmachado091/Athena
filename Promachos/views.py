from django.shortcuts import render
from django.views.generic.base import TemplateView

class HomeView(TemplateView):
	template_name = "teste_juiz.html"

class LoginView(TemplateView):
	template_name = "login.html"

# Create your views here.
