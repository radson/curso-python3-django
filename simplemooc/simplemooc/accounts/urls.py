from django.conf.urls import url
from django.contrib.auth import views as login_views
from . import views


urlpatterns = [
    # Recebe dicionário com parametros nomeados, substituindo o template padrão do Django pelo customizado.
    url(r'^entrar/$', login_views.login, {'template_name': 'accounts/login.html'}, name='login'), 
    url(r'^cadastre-se/$', views.register, name='register'),
]