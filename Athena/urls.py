from django.conf.urls import include, url
from django.contrib import admin

from Promachos import views as Promachos_views

urlpatterns = [
    # Examples:
    # url(r'^$', 'Athena.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^home$', Promachos_views.home),
    url(r'^login/$', 'Promachos.views.login'),
    url(r'^logout/$', 'Promachos.views.logout'),
    url(r'^cadastro/$', 'Promachos.views.register_user'),
]
