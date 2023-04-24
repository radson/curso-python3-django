from django.conf.urls import url
from django.contrib.auth import views as login_views
from . import views


urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
    # Recebe dicionário com parametros nomeados, substituindo o template padrão do Django pelo customizado.
    url(r'^entrar/$', login_views.login, {'template_name': 'accounts/login.html'}, name='login'),
    url(r'^sair/$', login_views.logout, {'next_page': 'core:home'}, name='logout'),
    url(r'^cadastre-se/$', views.register, name='register'),
]