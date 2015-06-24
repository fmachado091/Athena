from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    # Examples:
    # url(r'^$', 'Athena.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^home$', 'Promachos.views.home'),
    url(r'^login/$', 'Promachos.views.login'),
    url(r'^logout/$', 'Promachos.views.logout'),
    url(r'^cadastro/$', 'Promachos.views.register_user'),
    url(r'^professor/$', 'Promachos.views.professor'),
    url(r'^prof_ativ/$', 'Promachos.views.prof_ativ'),
    url(r'^aluno/$', 'Promachos.views.aluno'),
    url(r'^aluno_ativ/$', 'Promachos.views.aluno_ativ'),
]
