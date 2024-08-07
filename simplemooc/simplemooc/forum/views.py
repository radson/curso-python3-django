from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView, TemplateView, View

from .forms import ReplyForm
from .models import Reply, Thread

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
    template_name = 'forum/thread.html'

    def get(self, request, *args, **kwargs):
        response = super(ThreadView, self).get(request, *args, **kwargs)
        if not self.request.user.is_authenticated() or \
            (self.object.author != self.request.user):
            self.object.views = self.object.views + 1
            self.object.save()
        return response

    def get_context_data(self, **kwargs):
        context = super(ThreadView, self).get_context_data(**kwargs)
        context["tags"] = Thread.tags.all()
        context['form'] = ReplyForm(self.request.POST or None)
        return context

    def post(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated():
            messages.error(self.request, 'Para respondeu ao tópico é necessário estar logado.')
            return redirect(self.request.path)
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        form = context['form']
        if form.is_valid():
            reply = form.save(commit=False)
            reply.thread = self.object
            reply.author = self.request.user
            reply.save()
            messages.success(self.request, 'A sua resposta foi enviada com sucesso.')
            context['form'] = ReplyForm()
        return self.render_to_response(context)
    
class ReplyCorrectView(View):
    correct = True

    def get(self, request, pk):
        reply = get_object_or_404(Reply, pk=pk, thread__author=request.user)
        reply.correct = self.correct
        reply.save()
        messages.success(request, 'Resposta atualizada com sucesso.')
        return redirect(reply.thread.get_absolute_url())



index = ForumView.as_view()
thread = ThreadView.as_view()
reply_correct = ReplyCorrectView.as_view()
reply_incorrect = ReplyCorrectView.as_view(correct=False)