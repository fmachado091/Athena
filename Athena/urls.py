from django.conf.urls import patterns, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = patterns(
    '',
    (r'^admin/', include(admin.site.urls)),
    (r'^$', 'Promachos.views.login'),
    (r'^home$', 'Promachos.views.home'),
    (r'^login/$', 'Promachos.views.login'),
    (r'^logout/$', 'Promachos.views.logout'),
    (r'^cadastro/$', 'Promachos.views.register_user'),
    (r'^professor/$', 'Promachos.views.professor'),
    (r'^prof_ativ/(?P<id_ativ>[0-9]+)/$', 'Promachos.views.prof_ativ'),
    (r'^aluno/$', 'Promachos.views.aluno'),
    (
        r'^aluno/aluno_ativ/(?P<ativ_id>[0-9]+)/$',
        'Promachos.views.aluno_ativ'
    ),
    (r'^aluno/aluno_turmas/$', 'Promachos.views.aluno_turmas'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
