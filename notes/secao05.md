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

## 57. Página Inicial interna do Curso

### Objetivos

* Incluir no menu lateral links com mais detalhes dos cursos.

### Etapas

No model `Enrollment`, incluir uma propriedade para verificar se a inscrição está aprovada.

```Python
class Enrollment(models.Model):
    # omitido código sem alteração

    def is_approved(self):
        return self.status == 1

```

Na views da app `courses`, adicionar nova view `announcements`, que recebe a `slug` do curso e verifica se o usuário logado está com inscrição válida, retornando para a página de anuncios do curso:

```Python
# omitido código sem alteração
@login_required
def announcements(request, slug):
    course = get_object_or_404(Course, slug=slug)
    if not request.user.is_staff:
        enrollment = get_object_or_404(
            Enrollment, user=request.user, course=course)

        if not enrollment.is_approved():
            messages.error(request, "A sua inscrição está pendente.")
            return redirect('accounts:dashboard')

    template = 'courses/announcements.html'
    context = {
        'course': course
    }
    return render(request, template, context)
```

No arquivo de rotas `courses/urls.py` adicionar a nova url:

```Python
urlpatterns = [
    # omitido código sem alteração
    url(r'^(?P<slug>[\w_-]+)/anuncios/$',
        views.announcements, name='announcements'),
]
```

Criar o novo template em `courses/templates/courses/announcements.html`. Este template vai extender de `dashboard.html` e possuir um bloco para ser incluído no bloco do menu do `dashboard.html`, usando a tag `block.super`. Haverá também o bloco `dashboard_content` para o conteúdo do dashboard.

```Django
{% extends 'accounts/dashboard.html' %}

{% block menu_options %}
<li class="pure-menu-heading">
    {{ course }}
</li>
<li>
    <a href="#">
        <i class="fa fa-video-camera"></i> Aulas e Materiais
    </a>
</li>
<li>
    <a href="#">
        <i class="fa fa-info-circle"></i> Informações
    </a>
</li>
<li>
    <a href="#">
        <i class="fa fa-envelope"></i> Anúncios
    </a>
</li>
<li>
    <a href="#">
        <i class="fa fa-comments"></i> Fórum de Dúvidas
    </a>
</li>
{{ block.super }}
{% endblock menu_options %}

{% block dashboard_content %}
    <div class="well">
    </div>
{% endblock dashboard_content %}
```

No template `dashboard.html` será necessário algumas alterações para acomodar essa nova disposição:

* Após a declaração do bloco content, colocar a declaração da custom tag `load_my_courses` que carrega as inscrições.
* Dentro do menu incluir a declaração do bloco `menu_options` para permitir que o template `announcements.html` possa incluir seu conteúdo.
* Atualizar o link para os anuncios  do curso com a nova url criada.

```Django
{% block content %}
{% load_my_courses user as enrollments %}

<!-- omitido código sem alteração -->

<div class="pure-menu pure-menu-open">
    <ul>
        <li class="pure-menu-heading">Bem-vindo, {{ user }}</li>
        {% block menu_options %}
            <li class="pure-menu-heading">Cursos</li>
            {% for enrollment in enrollments %}
                <li><a href={% url 'courses:announcements' enrollment.course.slug %}><i class="fa fa-book"></i> {{ enrollment.course }} </a></li>
            {% empty %}
                <li>Você não está inscrito em um curso.</li>
            {% endfor %}
            <li class="pure-menu-heading">Conta</li>
            <li><a href="{% url 'accounts:edit' %}">
                <i class="fa-solid fa-cog"></i> Editar Conta</a></li>
            <li><a href="{% url 'accounts:edit_password' %}">
                <i class="fa-solid fa-lock"></i> Editar Senha</a></li>
        {% endblock menu_options %}
    </ul>
</div>

<!-- omitido código sem alteração -->

<a href={% url 'courses:announcements' enrollment.course.slug %} class="pure-button pure-button-primary">Acessar</a>
```

## 58. Cancelando a inscrição no curso

### Objetivos

* Implementando a funcionalidade de cancelar inscrição no curso.

### Etapas

No app `courses`, adicionar uma nova view para permitir cancelar inscrição. Aqui a lógica é parecida com a os do anuncios, primeiro busca o curso a partir da `slug` em seguida a inscrição a partir do `course` e do `user` logado.

```Python
# omitido código sem alteração
@login_required
def undo_enrollment(request, slug):
    course = get_object_or_404(Course, slug=slug)
    enrollment = get_object_or_404(
        Enrollment, user=request.user, course=course)

    if request.method == 'POST':
        enrollment.delete()
        messages.success(request, 'Inscrição cancelada com sucesso.')
        return redirect('accounts:dashboard')

    template = 'courses/undo_enrollment.html'
    context = {
        'enrollment': enrollment,
        'course': course,
    }

    return render(request, template, context)
```
No arquivo de rotas `courses/urls.py` adicionar a nova url:

```Python
urlpatterns = [
    # omitido código sem alteração
    url(r'^(?P<slug>[\w_-]+)/cancelar-inscricao/$',
        views.undo_enrollment, name='undo_enrollment'),
]
```

Criar o novo template em `courses/templates/courses/course_dashboard.html`. Este template vai extender de `dashboard.html` e possuir um bloco `menu_options` para ser incluído no bloco do menu do `dashboard.html`, usando a tag `block.super`, o conteúdo será movido do template `announcements.html`. Haverá também o bloco `breadcrumb` para indicar em qual página de curso está navegando no momento.

```Django
{% extends 'accounts/dashboard.html' %}

{% block breadcrumb %}
    {{ block.super }}
    <li>/</li>
    <li><a href="{% url 'courses:announcements' course.slug %}">{{ course }}</a></li>
{% endblock breadcrumb %}

{% block menu_options %}
<li class="pure-menu-heading">
    {{ course }}
</li>
<li>
    <a href="#">
        <i class="fa fa-video-camera"></i> Aulas e Materiais
    </a>
</li>
<li>
    <a href="#">
        <i class="fa fa-info-circle"></i> Informações
    </a>
</li>
<li>
    <a href="#">
        <i class="fa fa-envelope"></i> Anúncios
    </a>
</li>
<li>
    <a href="#">
        <i class="fa fa-comments"></i> Fórum de Dúvidas
    </a>
</li>
{{ block.super }}
{% endblock menu_options %}
```

O conteúdo do template `announcements.html` ficará como a seguir:

```Django
{% extends 'courses/course_dashboard.html' %}

{% block dashboard_content %}
    <div class="well">
    </div>
{% endblock dashboard_content %}
```

Criar o novo template em `courses/templates/courses/undo_enrollment.html`. Este template vai extender de `course_dashboard.html` e possuir um bloco `dashboard_content` para ser incluído no bloco do menu do `dashboard.html`. 

```Django
{% extends 'courses/course_dashboard.html' %}

{% block dashboard_content %}
<form action="" method="post">
    {% csrf_token %}
    <h3>Você deseja cancelar a inscrição deste curso?</h3>
    <div class="pure-controls">
        <button type="submit" class="pure-button pure-button-primary">Confirmar</button>
        <a href={% url 'courses:announcements' course.slug %} class="pure-button">Cancelar</a>
    </div>
</form>
{% endblock dashboard_content %}
```

Por fim, no template `dashboard.html`, incluir a nova URL.

```Django
<!-- omitido código sem alteração -->
<a href={% url 'courses:undo_enrollment' enrollment.course.slug %} class="pure-button pure-error">Cancelar</a>
```

## 59. Modelagem e Admin dos Anúncios

### Objetivos

* Implementar as páginas internas dos cursos. Primeiramente modelando o anuncio de cursos.

### Etapas

Na app `courses`, adicionar no arquivo `models.py` os models para Anúncios e Comentários

```Python
class Announcement(models.Model):
    course = models.ForeignKey(Course, verbose_name='Curso')
    title = models.CharField('Título', max_length=100)
    content = models.TextField('Conteúdo')
    created_at = models.DateTimeField(
        'Criado em', auto_now=False, auto_now_add=True)
    update_at = models.DateTimeField(
        'Atualizado em', auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Anúncio'
        verbose_name_plural = 'Anúncios'
        ordering = ['-created_at']


class Comment(models.Model):
    announcement = models.ForeignKey(
        Announcement, verbose_name='Anúncio', related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='usuário')
    comment = models.TextField('Comentário')
    created_at = models.DateTimeField(
        'Criado em', auto_now=False, auto_now_add=True)
    update_at = models.DateTimeField(
        'Atualizado em', auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'
        ordering = ['created_at']
```

Em seguida realizar a migração no banco de dados.

```Shell
python manage.py makemigrations
python manage.py migrate
```

No arquivo `admin.py`, incluir os models recem criados para permitir gerencimanento pela interface de administração e validar que o funcionamento.

```Python
from .models import Announcement, Comment, Course, Enrollment
# omitido código sem alteração

admin.site.register([Announcement, Comment, Enrollment])
```

Acessar a url `http://localhost:8000/admin`.

## 60. Listagem de Anúncios

### Objetivos

* Implementar listagem dos anuncios de cursos.

### Etapas

No model `Announcement`, adicionar o `related_name` na ForeignKey `course` para ser possível listar os anúncios a partir do curso.

```Python
class Announcement(models.Model):
    course = models.ForeignKey(
        Course, verbose_name='Curso', related_name='announcements')
    # omitido código sem alteração
```

Na view `announcements`, incluir a variável de contexto com todos os registros de anúncio de um curso.

```Python
def announcements(request, slug):
    # omitido código sem alteração
    context = {
        'course': course,
        'announcements': course.announcements.all()
```

No conteúdo do template `announcements.html` incluir um `for` para a variável `announcements` dentro do bloco `dashboard_content`. Neste caso faz-se o uso do das tags [with](https://docs.djangoproject.com/pt-br/1.11/ref/templates/builtins/#with) que faz o cache dos registros da variável `announcements` sem causar uma nova consulta no banco de dados. Além do uso da tag [pluralize](https://docs.djangoproject.com/pt-br/1.11/ref/templates/builtins/#pluralize) que retorna o sufixo de um valor se ele não for 1, por default acrescenta o 's'. 

```Django
{% extends 'courses/course_dashboard.html' %}

{% block dashboard_content %}
    {% for announcement in announcements %}
        <div class="well">
            <h2>{{ announcement.title }}</h2>
            {{ annoucemtent.content|linebreaks}}
            <p>
                <a href="#comments">
                    <i class="fa fa-comment"></i>
                    {% with announcement.comments.count as comments_count %}
                        {{ comments_count }}
                        Comentário{{ comments_count|pluralize }}
                    {% endwith %}
                </a>
            </p>
        </div>
    {% empty %}
        <div class="well">
            <h2>Nenhum anúncio criado.</h2>
        </div>
    {% endfor %}
{% endblock dashboard_content %}
```

Para testar deve-se adicionar alguns comentários através da interface de adminsitração do Django.

## 61. Página do Anúncio e Comentários

### Objetivos

* Implementar a página que exibe um anuncio e seus comentários.

### Etapas

Na app `courses` adicionar nova view que retornar os anúncios do curso. O trecho que busca o curso e a inscrição é o mesmo de views anteriores e poderá ser melhorado para evita repetição de código. Adicionalmente faz-se a busca do anúncio pelo curso e chave primária (pk), passando também no contexto.

```Python
from .models import Announcement
# omitido código sem alteração

@login_required
def show_announcement(request, slug, pk):
    course = get_object_or_404(Course, slug=slug)
    if not request.user.is_staff:
        enrollment = get_object_or_404(
            Enrollment, user=request.user, course=course)

        if not enrollment.is_approved():
            messages.error(request, "A sua inscrição está pendente.")
            return redirect('accounts:dashboard')

    announcement = get_object_or_404(course.announcements.all(), pk=pk)

    template = 'courses/show_announcements.html'
    context = {
        'course': course,
        'announcement': announcement
    }

    return render(request, template, context)
```

Atualizar arquivo de rotas, desta vez incluindo também o tratamento da pk na URL. 

```Python
urlpatterns = [
    url(r'^(?P<slug>[\w_-]+)/anuncios/(?P<pk>\d+)/$',
        views.show_announcement, name='show_announcement'),
]
```

Adicionar novo template em `courses/templates/courses/show_announcements.html`, este terá uma estrutura inicial parecida com `announcements.html`.  Neste template foi feito o uso do filtro [timesince](https://docs.djangoproject.com/pt-br/1.11/ref/templates/builtins/#timesince) que formata uma data como a hora desde essa data. 

```Django
{% extends 'courses/course_dashboard.html' %}

{% block dashboard_content %}
    <div class="well">
        <h2>{{ announcement.title }}</h2>
        {{ announcement.content|linebreaks }}
    </div>
    <div class="well">
        <h4 id="comments">Comentários
            <a href="#add_comment" class="fright"></a>
        </h4>
        <hr />
        {% for comment in announcement.comments.all %}
            <p>
                <strong>{{ comment.user }}</strong> disse à {{ comment.created_at|timesince }} atrás: <br>
                {{ comment.comment|linebreaksbr }}
            </p>
            <hr>
        {% empty %}
        <p>
            Nenhum comentário para este anúncio.
        </p>
        {% endfor %}
    </div>
{% endblock dashboard_content %}
```

Alterar o template `announcements.html` para incluir o link para a URL da view `show_announcement` no título e na âncora para os comentários.

```Django
<!-- omitido código sem alteração -->
<div class="well">
    <h2>
        <a href={% url 'courses:show_announcement' course.slug announcement.pk %}>
            {{ announcement.title }}
        </a>
    </h2>
    {{ annoucemtent.content|linebreaks}}
    <p>
        <a href="{% url 'courses:show_announcement' course.slug announcement.pk %}#comments">
            <!-- omitido código sem alteração -->
        </a>
    </p>
</div>
```

## 62. Comentando os Anúncios

### Objetivos

* Implementar form que permite cadastrar comentários.

### Etapas

No `forms.py` da app `courses` adicionar novo form herdando de ModelForm para inclusão de comentário:

```Python
from .models import Comment
# omitido código sem alteração

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
```

Em `views.py` modificar a view `show_announcement` para incluir o form. Na instancia do CommentForm, utilizou-se o `commit=False` (disponível apenas para ModelForm) que não salva imediatamente o registro no banco, ele vai fazer o save pegar os valores do formulário e passar para o objeto e retornar este objeto. Em seguida inclui-se o `user` e o `announcement` ai então faz-se o `save()`. Passa-se também o form para o contexto.

```Python
from .forms import CommentForm

# omitido código sem alteração
announcement = get_object_or_404(course.announcements.all(), pk=pk)
    form = CommentForm(request.POST or None)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.announcement = announcement
        comment.save()

        form = CommentForm()
        messages.success(request, 'Comentário enviado com sucesso.')

    template = 'courses/show_announcements.html'
    context = {
        'course': course,
        'announcement': announcement,
        'form': form,
    }

    return render(request, template, context)
```

No template `show_announcements.html` implementa-se o `form`, logo após o fim do `{% endfor %}` que exibe os `announcements`. 

```Django
{% extends 'courses/course_dashboard.html' %}

{% block breadcrumb %}
    {{ block.super }}
    <li>/</li>
    <li><a href="{% url 'courses:show_announcement' course.slug announcement.pk %}">{{ announcement }}</a></li>
{% endblock breadcrumb %}

<!-- omitido código sem alteração -->

{% endfor %}
<form method="post" class="pure-form pure-form-stacked" id="add_comment">
    {% csrf_token %}
    <fieldset>
        {{ form.non_field_errors }}
        {% for field in form %}
            <div class="pure-control-group">
                {{ field.label_tag }}
                {{ field }}
                {{ fiel.errors }}
            </div>
        {% endfor %}
        <div class="pure-controls">
            <button type="submit" class="pure-button pure-button-primary">Enviar</button>
        </div>
    </fieldset>
</form>
```

## 63. Usando signal para enviar e-mail

### Objetivos

* Notificar por e-mail quando houver anuncio usando o recurso [Signals](https://docs.djangoproject.com/en/1.11/topics/signals/) do Django.

### Etapas

Os sinais permitem que certos remetentes notifiquem um conjunto de receptores de que alguma ação ocorreu. 

Em `models.py`, adicionar um método para tratar o post_save de quando um anúncio é criado. A variável `instance` refere-se ao anúncio, para cada inscrição é no curso será enviado um e-mail para a conta associada informando de um novo anúncio, por isso verifica-se o `created`.

O signal `models.signals.post_save.connect` com a função `connect` faz a ligação entre o sinal e a função criada.

```Python
from simplemooc.core.mail import send_mail_template
# omitido código sem alteração

def post_save_announcement(instance, created, **kwargs):
    if created:
        subject = instance.title
        context = {
            'announcement': instance
        }

        template_name = 'courses/announcement_mail.html'
        enrollments = Enrollment.objects.filter(
            course=instance.course, status=1)

        for enrollment in enrollments:
            recipient_list = [enrollment.user.email]
            send_mail_template(subject, template_name, context, recipient_list)


models.signals.post_save.connect(
    post_save_announcement, sender=Announcement, 
    dispatch_uid='post_save_announcement')
```

Para o envio de e-mail, deve-se adicionar novo template em `courses/templates/courses/announcement_mail.html` mostrando apenas o conteúdo do anúncio.

```Django
{{ announcement.content|linebreaks }}
```

## 64. Modelagem das Aulas

### Objetivos

* Implementar modelagem para Aulas e Materiais.

### Etapas

No `models.py` da app `Courses` adicionar dois novos models para tratar das Aulas e Materiais chamados `Lesson` e `Material` que são relacionados entre si.

```Python
# omitido código sem alteração
class Lesson(models.Model):
    name = models.CharField("Nome", max_length=100)
    description = models.TextField('Descrição', blank=True)
    number = models.IntegerField('Número (ordem)', blank=True, default=0)
    release_date = models.DateField('Data de Liberação', blank=True, null=True)

    course = models.ForeignKey(
        Course, verbose_name='Curso', related_name='lessons')

    created_at = models.DateTimeField(
        'Criado em', auto_now=False, auto_now_add=True)
    update_at = models.DateTimeField(
        'Atualizado em', auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Aula'
        verbose_name_plural = 'Aulas'
        ordering = ['number']


class Material(models.Model):
    name = models.CharField("Nome", max_length=100)
    embedded = models.TextField('Vídeo embedded', blank=True)
    file = models.FileField(
        upload_to='lessons/materials', null=True, blank=True)

    lesson = models.ForeignKey(
        Lesson, verbose_name='aula', related_name='materials')

    def is_embedded(self):
        return bool(self.embedded)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Material'
        verbose_name_plural = 'Materiais'
```

Em seguida realizar a migração no banco de dados.

```Shell
python manage.py makemigrations
python manage.py migrate
```

## 65. Admin das Aulas

### Objetivos

* Implementar suporte para Aulas e Materiais no painel de adminsitração do Django

### Etapas

No `admin.py` adicionar modelagem criados anteriormente. A interface administrativa tem a capacidade de editar modelos na mesma página que um modelo pai. Estes são chamados de [inline](https://docs.djangoproject.com/pt-br/1.11/ref/contrib/admin/#django.contrib.admin.InlineModelAdmin). Para esta implementação será usado o modo `StackedInline`.

```Python
from .models import Lesson, Material

class MaterialInlineAdmin(admin.StackedInline):
    model = Material


class LessonAdmin(admin.ModelAdmin):
    list_display = ['name', 'number', 'course', 'release_date']
    search_fields = ['name', 'description']
    list_filter = ['created_at']

    inlines = [
        MaterialInlineAdmin
    ]

admin.site.register(Course, CourseAdmin)
admin.site.register([Announcement, Comment, Enrollment, Material])
admin.site.register(Lesson, LessonAdmin)
```

## 66. Decorator para Acesso ao Curso

### Objetivos

* Criar um decorator para promover reutilização do código que consulta o curso para as últimas views implementadas.

### Etapas

Na app `courses` adicionar o arquivo `decorators.py` que irá conter a lógica de validação se um usuário tem permissão para visualizar um curso.

```Python
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect

from .models import Course, Enrollment

def enrollment_required(view_func):
    def _wrapper(request, *args, **kwargs):
        slug = kwargs['slug']
        course = get_object_or_404(Course, slug=slug)
        has_permission = request.user.is_staff

        if not has_permission:
            try:
                enrollment = Enrollment.objects.get(
                    user=request.user, course=course
                )
            except Enrollment.DoesNotExist:
                message = 'Desculpe, mas você não tem permissão para ' \
                    + 'acessar esta página'
            else:
                if enrollment.is_approved():
                    has_permission = True
                else:
                    message = 'A sua inscrição no curso ainda está ' \
                        + 'está pendente.'

        if not has_permission:
            messages.error(request, message)
            return redirect('accounts:dashboard')

        request.course = course
        return view_func(request, *args, **kwargs)
```

No arquivo `views.py`, realizar as alterações para remover o código anteriormente duplicado e fazer uso do novo decorator. Nas views em que o código duplicado foi removido, o valor do curso agora será consultado no request que o decorator enviou.

```Python
from .decorators import enrollment_required

@login_required
@enrollment_required
def announcements(request, slug):
    course = request.course

    template = 'courses/announcements.html'
    context = {
        'course': course,
        'announcements': course.announcements.all()
    }
    return render(request, template, context)

@login_required
@enrollment_required
def show_announcement(request, slug, pk):
    course = request.course

    announcement = get_object_or_404(course.announcements.all(), pk=pk)
    form = CommentForm(request.POST or None)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.announcement = announcement
        comment.save()

        form = CommentForm()
        messages.success(request, 'Comentário enviado com sucesso.')

    template = 'courses/show_announcements.html'
    context = {
        'course': course,
        'announcement': announcement,
        'form': form,
    }

    return render(request, template, context)
```

## 67. Listagem das Aulas

### Objetivos

* Implementar a listagem das aulas.

### Etapas

No `models.py` da app `courses`, implementar uma propriedade nos models `Courses` e `Lessons` para verificar se a aula está de acordo com a data de liberação cadastrada.

```Python
from django.utils import timezone

class Course(models.Model):
# omitido código sem alteração

    def release_lessons(self):
        today = timezone.now().date()
        return self.lessons.filter(release_date__gte=today)


class Lesson(models.Model):
# omitido código sem alteração
    def is_available(self):
        if self.release_date:
            today = timezone.now().date()
            return self.release_date >= today
        return False
```

Adicionar nova view `lessons` que retorna as aulas de um curso e a view `lesson` para retornar uma aula específica a partir da `pk`.

```Python
from .models import Lesson
# omitido código sem alteração

@login_required
@enrollment_required
def lessons(request, slug):
    course = request.course
    lessons = course.release_lessons()

    if request.user.is_staff:
        lessons = course.lessons.all()

    template = 'courses/lessons.html'
    context = {
        'course': course,
        'lessons': lessons
    }

    return render(request, template, context)


@login_required
@enrollment_required
def lesson(request, slug, pk):
    course = request.course
    lesson = get_object_or_404(Lesson, pk=pk, course=course)

    if not request.user.is_staff and not lesson.is_available():
        messages.error(request, 'Esta aula não está disponivel')
        return redirect('courses:lessons', slug=course.slug)

    template = 'courses/lesson.html'
    context = {
        'course': course,
        'lesson': lesson
    }

    return render(request, template, context)
```

Atualizar rotas em `urls.py` para as novas views, sendo que `lesson` recebe o parâmetro nomeado `pk` que pode ser 1 ou mais dígitos.

```Python
urlpatterns = [
    # omitido código sem alteração
    url(r'^(?P<slug>[\w_-]+)/aulas/$', views.lessons, name='lessons'),
    url(r'^(?P<slug>[\w_-]+)/aulas/(?P<pk>\d+)/$', views.lesson, name='lesson'),
]
```

Criar os novos templates `lessons.html` e `lesson.html` em `courses/templates/courses/`. Ambos vão extender de `course_dashboard.html`. Neste template utilizou-se a tag filter [truncatewords](https://docs.djangoproject.com/pt-br/1.11/ref/templates/builtins/#truncatewords) que trunca uma string depois de certo número de caracteres.

Conteúdo de `lessons.html`

```Django
{% extends 'courses/course_dashboard.html' %}

{% block dashboard_content %}
    {% for lesson in lessons %}
        <div class="well">
            <h2> <a href={% url 'courses:lesson' course.slug lesson.pk %}>{{ lesson }}</a> </h2>
            <p>
                {{ lesson.description|truncatewords:'20'}}
                <br>
                <a href={% url 'courses:lesson' course.slug lesson.pk %}>
                    <i class="fa fa-eye"></i>
                    Acessar Aula
                </a>
            </p>
        </div>
    {% empty%}
        <div class="well">
            <h2>
                Nenhuma aula disponível.
            </h2>
        </div>
    {% endfor %}
{% endblock dashboard_content %}
```

Conteúdo inicial  de `lesson.html`, o restante será implementado na próxima aula.

```Django
{% extends 'courses/course_dashboard.html' %}

{% block dashboard_content %}

{% endblock dashboard_content %}
```

No template `course_dashboard.html`, atualizar as urls para aulas e anuncios.

```Django
<!-- omitido código sem alteração -->
<li>
    <a href={% url 'courses:lessons' course.slug %}>
        <i class="fa fa-video-camera"></i> Aulas e Materiais
    </a>
</li>
<!-- omitido código sem alteração -->
<li>
    <a href={% url 'courses:announcements' course.slug %}>
        <i class="fa fa-envelope"></i> Anúncios
    </a>
</li>
<!-- omitido código sem alteração -->
```

## 68. Exibição do Material (embedded)

### Objetivos

* Implementar a exibição do conteúdo da aula (arquivos e embedded).

### Etapas

Adicionar nova view `material`, nela há uma verificação se não for `embedded`, retorna a url do arquivo para baixar.

```Python
from .models import  Material
# omitido código sem alteração

@login_required
@enrollment_required
def material(request, slug, pk):
    course = request.course
    material = get_object_or_404(Material, pk=pk, lesson__course=course)
    lesson = material.lesson

    if not request.user.is_staff and not lesson.is_available():
        messages.error(request, 'Este material não está disponivel')
        return redirect('courses:lesson', slug=course.slug, pk=lesson.pk)

    if not material.is_embedded():
        return redirect(material.file.url)

    template = 'courses/material.html'
    context = {
        'course': course,
        'lesson': lesson,
        'material': material
    }

    return render(request, template, context)
```

Criar o novo template em `courses/templates/courses/material.html`. Possui a mesma estrutura dos anteriores, neste template faz-se o uso da tag filter [safe](https://docs.djangoproject.com/pt-br/1.11/ref/templates/builtins/#safe) que escapa o conteúdo do campo `embedded`. Neste caso, para fins didáticos, não foram consideradas medidas de segurança mais restritas, porém é uma boa prática pra evitar código malicioso.

```Django
{% extends 'courses/course_dashboard.html' %}

{% block breadcrumb %}
    {{ block.super }}
    <li>/</li>
    <li><a href="{% url 'courses:lessons' course.slug %}">Aulas</a></li>
    <li>/</li>
    <li><a href="{% url 'courses:lesson' course.slug  lesson.pk %}">{{ lesson }}</a></li>
    <li>/</li>
    <li><a href="{% url 'courses:material' course.slug  material.pk %}">{{ material }}</a></li>
{% endblock breadcrumb %}

{% block dashboard_content %}
<div class="well">
    <h2><a href="{% url 'courses:material' course.slug  material.pk %}">{{ material }}</a></h2>
    {{ material.embedded|safe }}
    <p>
        <a href="{% url 'courses:lesson' course.slug  lesson.pk %}">Voltar</a>
    </p>
</div>

{% endblock dashboard_content %}
```

Atualizar rotas em `urls.py` para nova view.

```Python
urlpatterns = [
    # omitido código sem alteração
    url(r'^(?P<slug>[\w_-]+)/materiais/(?P<pk>\d+)/$',
        views.material, name='material'),
]
```

Adicionar o conteúdo do template `lesson.html`. Aqui foi utilizada a tag filter [cycle](https://docs.djangoproject.com/pt-br/1.11/ref/templates/builtins/#cycle) que faz alternância dos parametros dentro de um for, neste caso para produzir o efeito de zebrado da tabela, alternando a class da tag `tr`.

```Django
{% extends 'courses/course_dashboard.html' %}

{% block breadcrumb %}
    {{ block.super }}
    <li>/</li>
    <li><a href="{% url 'courses:lessons' course.slug %}">Aulas</a></li>
    <li>/</li>
    <li><a href="{% url 'courses:lesson' course.slug  lesson.pk %}">{{ lesson }}</a></li>
{% endblock breadcrumb %}

{% block dashboard_content %}
    <div class="well">
        <h2><a href="{% url 'courses:lesson' course.slug  lesson.pk %}">{{ lesson }}</a></h2>
        {{ lesson.description|linebreaks }}
        <p>
            <h4>Matereial da Aula</h4>
            <table class="pure-table full">
                <thead>
                    <tr>
                        <th>
                            Nome
                        </th>
                        <th>
                            Ação
                        </th>
                    </tr>
                </thead>
                <tbody>
                    {% for material in lesson.materials.all %}
                        <tr class={% cycle '' 'pure-table-odd' %}>
                            <td>
                                {{ material }}
                            </td>
                            <td>
                                {% if material.is_embedded %}
                                    <a href={% url 'courses:material' course.slug  material.pk %}>
                                        <i class="fa fa-video-camera"></i>
                                        Acessar
                                    </a>
                                {% else %}
                                    <a target="_blank" href="{{ material.file.url }}">
                                        <i class="fa fa-download"></i>
                                        Baixar
                                    </a>
                                {% endif %}
                            </td>
                        </tr>
                    {% endfor %}
                </tbody>
            </table>
        </p>
    </div>
    
{% endblock dashboard_content %}
```

No template `lessons.html` foi adicionado o `breadcrumb` antes do bloco `dashboard_content`.

```Django
{% block breadcrumb %}
    {{ block.super }}
    <li>/</li>
    <li><a href="{% url 'courses:lessons' course.slug %}">Aulas</a></li>
{% endblock breadcrumb %}
```