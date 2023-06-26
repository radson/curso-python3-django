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

## 55. Usando Custom Template Tags

### Objetivos

* Melhorar a navegação do usuário entre os cursos inscritos, criando [template tags customizadas](https://docs.djangoproject.com/en/1.8/howto/custom-template-tags/) com funcinalidades específicas.

### Etapas

* O Django reconhece o diretório com nome `templatetags` como um módulo que  The app should contain a templatetags directory, at the same level as models.py, views.py, etc. If this doesn’t already exist, create it - don’t forget the __init__.py file to ensure the directory is treated as a Python package.

Na view `dashboard` do app `accounts`, incluir uma variável de contexto que irá retornar todos os cursos que o user logado está inscrito.

```Python
from simplemooc.courses.models import Enrollment
 # omitido código sem alteração

@login_required
def dashboard(request):
    template_name = 'accounts/dashboard.html'
    context = {}
    context['enrollments'] = Enrollment.objects.filter(user=request.user)

    return render(request, template_name, context)
```

No template `dashboard.html`, na div que contém o menu, implementar o uso da variável `enrollments` com os cursos encontrados.

```Django
 <div class="pure-menu pure-menu-open">
    <ul>
        <li class="pure-menu-heading">Meus Cursos</li>
        {% for enrollment in enrollments %}
            <li><a href="#"> {{ enrollment.course }} </a></li>
        {% empty %}
            <li>Você não está inscrito em um curso.</li>
        {% endfor %}
        <li class="pure-menu-heading">Minha Conta</li>
        <li><a href="{% url 'accounts:edit' %}">Editar Conta</a></li>
        <li><a href="{% url 'accounts:edit_password' %}">Editar Senha</a></li>
    </ul>
</div>
```

Esta primeira abordagem poderá apresentar inconsistências ao navegar em outras páginas da aplicação que compartilham do mesmo menu mas que não tem a mesma variável de contexto. Repetir o código implementando esta variável em outras views não seria uma boa prática. Para isso que será utilizado o recurso de custom template tags.

Na app `courses` no mesmo nível de `models.py`, criar o diretório `templatetags` como um módulo Python (incluir arquivo `__init__.py` dentro do diretório criado).  Dentro do `templatetags` criar o arquivo `courses_tags.py` que conterá o código para a custom tag. Será uma tag de inclusão de código, que quando for invocada em um template irá inserir o código definido no templatetag.

```Bash
mkdir -p simplemooc/courses/templatetags
> simplemooc/courses/templatetags/__init__.py
> simplemooc/courses/templatetags/courses_tags.py
```

Em `courses_tags.py`, criar o método `my_courses` e registra-lo como tag usando o decorator `register`, que usará o método `inclusion_tag`, definindo o caminho do template a ser inserido. Este método retorna uma variável de contexto com os cursos.

```Python
from django.template import Library

from simplemooc.courses.models import Enrollment

register = Library()

@register.inclusion_tag('courses/templatetags/my_courses.html')
def my_courses(user):
    enrollments = Enrollment.objects.filter(user=user)
    context = {
        'enrollments': enrollments
    }

    return context
```

Criar em `simplemooc/courses/templates/templatetags/my_courses.html` o código do template que deverá ser incluído. É o mesmo código definido anteriormente em `dashboard.html`.

```Django
<li class="pure-menu-heading">Meus Cursos</li>
{% for enrollment in enrollments %}
    <li><a href="#"> {{ enrollment.course }} </a></li>
{% empty %}
    <li>Você não está inscrito em um curso.</li>
{% endfor %}
```

No template `dashboard.html` o código anteriormente definido, pode ser alterado para a forma a seguir:

```Django
{% load courses_tags %}
<!-- omitido código sem alteração -->
<div class="pure-menu pure-menu-open">
    <ul>
        {% my_courses user %}

        <!-- omitido código sem alteração -->
    </ul>
</div>
```

Neste techo acima, carregando o `courses_tags`, pode-se fazer uso da tag `my_courses` passando como parametro o usuário logado. Com isso, o trecho de código que está no template `my_courses.html` é inserido no HTML.

Outra abordagem mais flexível é registrar uma tag com `assignment_tag` que permite passar apenas a variável de contexto com os dados desejados sem o HTML. 

Em `courses_tags.py`, criar o método `load_my_courses` e registra-lo com `assignment_tag`. Este método retorna uma variável de contexto com os cursos.

```Python
# omitido código sem alteração

@register.assignment_tag()
def load_my_courses(user):
    return Enrollment.objects.filter(user=user)
```

No template `dashboard.html` o código voltaria a ser como no início, com a diferença de que será necessário carregar a tag `load_my_courses` como a variável `enrollments`, conforme forma a seguir:

```Django
<div class="pure-menu pure-menu-open">
    <ul>
        {% load_my_courses user as enrollments %}
        <li class="pure-menu-heading">Meus Cursos</li>
        {% for enrollment in enrollments %}
            <li><a href="#"> {{ enrollment.course }} </a></li>
        {% empty %}
            <li>Você não está inscrito em um curso.</li>
        {% endfor %}
        <!-- omitido código sem alteração -->
    </ul>
</div>
```

Ambas abordagens atendem ao propósito desta aula, ficando a critério de cada cenário qual escolher. 

## 56. Ajustando Design do Dashboard

### Objetivos

* Realizando melhorias de design no Dashboard.

### Etapas

Para melhorar o visual, serão utilizados os recursos da biblioteca de ícones [Font Awesome](https://fontawesome.com/). Para fins de desenvolvimento será realizada a instalação local, baixando o pacote de ícones para Web e usando a [instalação alternativa](https://fontawesome.com/docs/web/setup/host-yourself/webfonts#alternate-install-using-all-css).

Após baixar o pacote, extrair o diretório `webfonts` para `core/static/css/` e o arquivo `all.css` para `core/static/css/fontawesome/all.css`.

No template `base.html` fazer referência ao arquivo de estilo:

```Html
<link rel="stylesheet" href="{% static 'css/fontawesome/all.css' %}" />
```
No template `dashboard.html`, alterar adicionando referência aos ícones do font awesome na parte do menu. Na parte do conteúdo do Dashboard, incluir a listagem dos cursos e detalhes do curso usando a variável de contexto `enrollments`.

```Django
<div class="pure-u-1-3">
    <div class="pure-menu pure-menu-open">
        <ul>
            <li class="pure-menu-heading">Bem-vindo, {{ user }}</li>
            {% load_my_courses user as enrollments %}
            <li class="pure-menu-heading">Cursos</li>
            {% for enrollment in enrollments %}
                <li><a href="#"><i class="fa-solid fa-book-open-reader"></i> {{ enrollment.course }} </a></li>
            {% empty %}
                <li>Você não está inscrito em um curso.</li>
            {% endfor %}
            <li class="pure-menu-heading">Conta</li>
            <li><a href="{% url 'accounts:edit' %}">
                <i class="fa-solid fa-user-pen"></i> Editar Conta</a></li>
            <li><a href="{% url 'accounts:edit_password' %}">
                <i class="fa-solid fa-lock"></i> Editar Senha</a></li>
        </ul>
    </div>
</div>
<div class="pure-u-2-3">
    <div class="inner">
        {% block dashboard_content %}
            <h2>Meus Cursos</h2>
            {% for enrollment in enrollments %}
            <div class="well">
                <h3>{{ enrollment.course }} ({{ enrollment.course.start_date|date:'d/m/Y'|default:'Não informado' }})</h3>
                <p>{{ enrollment.course.description|linebreaks }}</p>
                <div class="pure-controls">
                    <a href="#" class="pure-button pure-button-primary">Acessar</a>
                    <a href="#" class="pure-button pure-error">Cancelar</a>
                </div>
            </div>
            {% empty %}
            <aside class="pure-u-1">
                <p>Nenhum curso inscrito.</p>
            </aside>
            {% endfor %}
        {% endblock dashboard_content %}
    </div>
</div>
```