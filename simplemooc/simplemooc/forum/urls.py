from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^tag/(?P<tag>[\w_-]+)/$', views.index, name='index_tagged'),
    url(r'^respostas/(?P<pk>\d+)/correta/$', views.reply_correct, name='reply_correct'),
    url(r'^respostas/(?P<pk>\d+)/incorreta/$', views.reply_incorrect, name='reply_incorrect'),
    url(r'^topico/(?P<slug>[\w_-]+)/$', views.thread, name='thread'),
]