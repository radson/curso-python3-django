# Seção 5: Acessando o Curso

## 52. Modelagem da Inscrição

### Objetivos

* Iniciar o desenvolvimento das aplicações do domínio do curso (ex. aulas, inscrições, etc). Nesta aula será criado o model de inscrições

### Etapas

No `models.py` da app `Courses` adicionar um novo model para tratar das inscrições chamado `Enrollment`.

```Python
from django.conf import settings

# omitido código sem alteração

class Enrollment(models.Model):

    STATUS_CHOICE = (
        (0, 'Pendente'),
        (1, 'Aprovado'),
        (2, 'Cancelado'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             verbose_name='Usuário', related_name='enrollments')

    course = models.ForeignKey(Course, verbose_name='enrollments')

    status = models.IntegerField(
        'Situação', choices=STATUS_CHOICE, default=0, blank=True)
    created_at = models.DateTimeField(
        'Criado em', auto_now=False, auto_now_add=True)
    update_at = models.DateTimeField(
        'Atualizado em', auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name = 'Inscrição'
        verbose_name_plural = 'Inscrições'
        unique_together = (('user', 'course'),)
```

Em seguida realizar a migração no banco de dados.

```Shell
python manage.py makemigrations
python manage.py migrate
```

## 53. Implementando a inscrição no Curso

### Objetivos

* Prapara o sistema para permitir a inscrição do usuário em um curso.

### Etapas

Na app `courses` adicionar em `views.py` nova view para permitir inscrição no curso. Esta view usa a `slug` do curso para selecionar o curso no banco de dados

```Python
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from .models import Enrollment

# omitido código sem alteração

@login_required
def enrollment(request, slug):
    course = get_object_or_404(Course, slug=slug)
    enrollment, created = Enrollment.objects.get_or_create(
        user=request.user, course=course)

    return redirect('accounts:dashboard')
```

No model `Enrollment`, alterar o valor default do campo `status` 1 (aprovado). Posteriormente uma lógica pode ser adicionada para tratar melhor.

```Python
# omitido código sem alteração
status = models.IntegerField(
        'Situação', choices=STATUS_CHOICE, default=1, blank=True)
```

No arquivo de rotas `urls.py` adicionar nova rota para inscrição

```Python
urlpatterns = [
    # omitido código sem alteração
    url(r'^(?P<slug>[\w_-]+)/inscricao/$', views.enrollment, name='enrollment'),
]
```

No template `details.html`, na tag que contem a label *Inscreva-se*, adicionar a url passando a slug como parâmetro.

```Django
<a href={% url 'courses:enrollment' course.slug %} class="pure-button primary-button">Inscreva-se</a>
```

## 54. Usando o django.contrib.messages

### Objetivos

* Usando a app chamada *messages* do Django para para mostrar notificações ao usuário.

### Etapas

Este app já vem habilitado por padrão no Django, no arquivo `settings.py`. 

```Python
INSTALLED_APPS = [
    'django.contrib.messages',
]
```

Na documentação do Django chama de [messages framework](https://docs.djangoproject.com/en/1.8/ref/contrib/messages/), e apresenta mais detalhes de uso, inclusive com o uso de TAGs para identificar o nível da mensagem (Sucesso, erro, info, debug, etc).

No `views.py` da app `courses`, importa-se o módulo messages e na view `enrollment` adiciona-se o comportamento da view para quando é uma nova inscrição ou quando já se está inscrito.

```Python
from django.contrib import messages
# omitido código sem alteração

@login_required
def enrollment(request, slug):
    course = get_object_or_404(Course, slug=slug)
    enrollment, created = Enrollment.objects.get_or_create(
        user=request.user, course=course)

    if created:
        messages.success(request, 'Você foi inscrito no curso com sucesso')
    else:
        messages.info(request, 'Você já está inscrito no curso')

    return redirect('accounts:dashboard')
```

No arquivo `base.html`, dentro da div `content` antes do block `content`, pode-se fazer uma iteração na variável `messages` que contém todas as mensagens. Desse modo ficará disponível para todos os templates que extendem de base.

```Django
<div class="content">
    <div class="pure-g-r content-ribbon">
        <aside class="pure-u-1">
            {% if messages %}
                {% for message in messages %}
                    <p>{{ message }}</p>
                {% endfor %}
            {% endif %}
        </aside>
    </div>
    {% block content %}{% endblock content %}
</div>
```

Uma outra aplicação é na view `edit` do app `accounts`, onde antes utilizava-se uma variável de contexto para indicar sucesso e a limpeza do form, agora pode-se usar o framework de mensagens e usar um redirect para o dashboard.

```Python
from django.contrib import messages
# omitido código sem alteração

def edit(request):
    template_name = 'accounts/edit.html'
    context = {}

    if request.method == 'POST':
        form = EditAccountForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Os dados da sua conta foram alterados com sucesso.')
            return redirect('accounts:dashboard')
    else:
        # omitido código sem alteração
```

No template `edit.html` do app `accounts`, pode-se remover a verificação da existência da varivável de contexto `success`, ficando como a seguir:

```Django
<!-- omitido código sem alteração -->
{% block dashboard_content %}
<form class="pure-form pure-form-stacked" method="post">
    {% csrf_token %}
    <fieldset>

<!-- omitido código sem alteração -->
```