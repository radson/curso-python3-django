from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView

from .models import Thread

# Implementação mantida da aula 77. para referencia
# class ForumView(TemplateView):
#     template_name = 'forum/index.html'


class ForumView(ListView):
    paginate_by = 2
    template_name = 'forum/index.html'

    def get_context_data(self, **kwargs):
        context = super(ForumView, self).get_context_data(**kwargs)
        context["tags"] = Thread.tags.all()
        return context

    def get_queryset(self):
        queryset = Thread.objects.all()
        order = self.request.GET.get('order', '')

        if order == 'views':
            queryset = queryset.order_by('-views')
        elif order == 'answers':
            queryset = queryset.order_by('-answers')
        
        tag = self.kwargs.get('tag', '')

        if tag:
            queryset = queryset.filter(tags__slug__icontains=tag)

        return queryset
    

class ThreadView(DetailView):
    model = Thread
    template_name = 'forum/thread.hml'
    

index = ForumView.as_view()
thread = ThreadView.as_view()