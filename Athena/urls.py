from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    # Examples:
    # url(r'^$', 'Athena.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'Promachos.views.login'),
    url(r'^home$', 'Promachos.views.home'),
    url(r'^login/$', 'Promachos.views.login'),
    url(r'^logout/$', 'Promachos.views.logout'),
    url(r'^cadastro/$', 'Promachos.views.register_user'),
    url(r'^professor/$', 'Promachos.views.professor'),
    url(r'^prof_ativ/(?P<id_ativ>[0-9]+)/$', 'Promachos.views.prof_ativ'),
    url(r'^aluno/$', 'Promachos.views.aluno'),
    url(r'^aluno/aluno_ativ/(?P<ativ_id>[0-9]+)/$',
        'Promachos.views.aluno_ativ'),
    url(r'^aluno/aluno_turmas/$', 'Promachos.views.aluno_turmas'),
]
