from django.shortcuts import render
from django.views.generic import ListView, TemplateView

from .models import Thread

# Implementação mantida da aula 77. para referencia
# class ForumView(TemplateView):
#     template_name = 'forum/index.html'


class ForumView(ListView):
    model = Thread
    paginate_by = 10
    template_name = 'forum/index.html'

    def get_context_data(self, **kwargs):
        context = super(ForumView, self).get_context_data(**kwargs)
        context["tags"] = Thread.tags.all()
        return context
    

index = ForumView.as_view()