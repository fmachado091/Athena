from django.conf.urls import include, url
from django.contrib import admin

from Promachos import views as Promachos_views

urlpatterns = [
    # Examples:
    # url(r'^$', 'Athena.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^home$', Promachos_views.home),
    url(r'^login/$', 'Promachos.views.login_promachos'),
    url(r'^auth/$',  'Promachos.views.auth_view_promachos'),    
    url(r'^logout/$', 'Promachos.views.logout_promachos'),
    url(r'^aluno/$', 'Promachos.views.loggedin_promachos'),
    url(r'^invalido/$', 'Promachos.views.invalid_login_promachos'),    
    url(r'^cadastro/$', 'Promachos.views.register_user_promachos'),
    url(r'^registro_sucesso/$', 'Promachos.views.register_success_promachos'),
]
