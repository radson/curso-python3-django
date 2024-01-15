# Seção 7: Fórum de Dúvidas

## 75. Modelagem do Fórum

### Objetivos

* Criar um app de Forum de Dúvidas sobre os cursos
* Utilizar bibliotecas criadas por terceiros para reaproveitar o código. Será integrada lib django-taggit

### Etapas

Com o venv habilitado, baixar a versão da lib django-taggit compatível com Django 1.11 utilizado neste projeto.

```Bash
pip install django-taggit==1.4.0
```

Integrar a lib ao projeto Django, adicionando a app `taggit` em `INSTALLED_APPS` no arquivo `settings.py`.

```Python
INSTALLED_APPS = [
    # outras apps instaladas foram omitidas
    'taggit',
]
```

Finaliar a instalação rodando as migrations necessárias ao taggit.

```Shell
python manage.py migrate
```

Agora criar nova app com nome 'Forum' dentro da estrutura do projeto `simplemooc`.

```Bash
mkdir simplemooc/forum
python manage.py startapp forum simplemooc/forum
```

Criar a modelagem da app Forum no arquivo `models.py` com dois objetos principais: Thread e Reply. 
O uso da lib taggit é através do campo `tags` que recebe um `TaggableManager`.

```Python
from django.conf import settings
from django.db import models
from taggit.managers import TaggableManager


class Thread(models.Model):

    title = models.CharField('Título', max_length=100)
    body = models.TextField('Mensagem')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Autor',
        related_name='threads'
        )
    views = models.IntegerField('Visualizações', blank=True, default=0)
    answers = models.IntegerField('Respostas', blank=True, default=0)
    tags = TaggableManager()
    
    created = models.DateField('Criado em', auto_now_add=True)
    modified = models.DateField('Modificado em', auto_now=True)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Tópico'
        verbose_name_plural = 'Tópicos'
        ordering = ['-modified']

class Reply(models.Model):

    reply = models.TextField('Resposta')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Autor',
        related_name='replys'
        )
    correct = models.BooleanField('Correta?', blank=True, default=False)

    created = models.DateField('Criado em', auto_now_add=True)
    modified = models.DateField('Modificado em', auto_now=True)        

    def __str__(self):
        return self.reply[:100]

    class Meta:
        verbose_name = 'Resposta'
        verbose_name_plural = 'Respostas'
        ordering = ['-correct', 'created']
```

## 76. Class-based views no Fórum Parte 1

### Objetivos

* Iniciar a implementação das views
* Conhecer a class-based views

### Etapas

Para implementar uma view a partir de um model, pode-se utilizar o recurso  `Base views` do Django. Mais detalhes na documentação sobre [Base Views](https://docs.djangoproject.com/en/1.11/ref/class-based-views/base/#base-views).

Iniciar a implementação no arquivo `views.py`, utilizando a classe [TemplateView](https://docs.djangoproject.com/en/1.11/ref/class-based-views/base/#templateview).

```Python
from django.shortcuts import render
from django.views.generic import TemplateView


class ForumView(TemplateView):
    template_name = 'forum/index.html'
```

Criar o diretório para templates

```Bash
mkdir -p forum/templates/forum
> forum/templates/forum/index.html
```

Criar o `urls.py` na app Forum informando a view index

```Python
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
```

Instalar a app Forum em settings e realizar a migração que faltou na aula anterior.

```Python
INSTALLED_APPS = [
    # outras apps instaladas foram omitidas
    'simplemooc.forum',
]
```

Criar e executar as migrates.

```Shell
python manage.py makemigrations
python manage.py migrate
```

## 77. Class-based views no Fórum Parte 2

### Objetivos

* Continuar a implementação das views

### Etapas

No arquivo `urls.py` do projeto, adicionar a referência ao `urls.py` da app `forum`.

```Python
urlpatterns = [
    # omitido código anterior
    url(r'^forum/', include('simplemooc.forum.urls', namespace='forum')),
]
```

No arquivo `views.py` da app `forum`, não existe a definição do `index` conforme consta no arquivo `urls.py` da app, para isso será necessário definir o `index` que recebe uma instãncia de `ForumView` com `as_view()`, que retornar uma função para `index`.

```Python
from django.shortcuts import render
from django.views.generic import TemplateView


class ForumView(TemplateView):
    template_name = 'forum/index.html'

index = ForumView.as_view()
```

## 78. Listagem dos Tópicos 1

### Objetivos

* Utilizando a ListView para listar Tópicos.

### Etapas

A [ListView](https://docs.djangoproject.com/en/1.11/ref/class-based-views/generic-display/#listview) é uma classe do Django que serve para listagem de objetos.

No arquivo `views.py`, alterar a implementação da view `ForumView`, indicando o model, a quantidade de registros por página e o nome do template.

```Python
# Omitido imports anteriores
from django.views.generic import ListView
from .models import Thread

# Implementação mantida da aula 77. para referencia
# class ForumView(TemplateView):
#     template_name = 'forum/index.html'

class ForumView(ListView):
    model = Thread
    paginate_by = 10
    template_name = 'forum/index.html'

index = ForumView.as_view()
```

Realizar os ajustes em `index.html` com as seguintes modificações:
* Incluir as URLS para página de início e do fórum
* Adicionar codigo que exibe as informações sobre os tópicos, retornados no objetvo `object_list` do `ListView`. Adicionados os filtros `pluralize` e `timesince` para auxiliar na exibição das informações.

```Django
<!-- omitido código não modificado -->
<ul class="breadcrumb">
    <li><a href={% url "core:home" %}>Início</a></li>
    <li>/</li>
    <li><a href={% url "forum:index" %}>Fórum de Discussões</a></li>
</ul>

<!-- omitido código não modificado -->

<div class="inner">
    {% for thread in object_list %}   
        <div class="well">
            <h3><a href="" title="">{{ thread.title }}</a></h3>
            <h5>
                Criado por {{ thread.author }} 
                | {{ thread.answers }}  resposta{{ thread.answers|pluralize }}
                | {{ thread.views }} visualizaç{{ thread.views|pluralize:"ão,ões" }} 
            </h5>
            <p>
                <i class="fa fa-tags"></i>
                Tags: 
                {% for tag in thread.tags.all %}
                    <a href="">{{ tag }}</a>
                    {% if not forloop.last %},{% endif %}
                {% endfor %}
                <a class="fright" href="" title="">
                    Atualizado a {{ thread.modified|timesince }} atrás
                </a>
            </p>
        </div>
    {% endfor %}
    <!-- omitido código não modificado -->
</div>

```

Declarar os models no `admin.py` do app `Forum`, para permitir cadastrar e listar registros nesses models pela interface de admin.

```Python
from django.contrib import admin

from .models import Reply, Thread


class ThreadAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created', 'modified']
    search_fields = ['title', 'author__email', 'body']

class ReplyAdmin(admin.ModelAdmin):
    list_display = ['thread', 'author', 'created', 'modified']
    search_fields = ['thread__title', 'author__email', 'reply']

admin.site.register(Thread, ThreadAdmin)
admin.site.register(Reply, ReplyAdmin)
```

Corrigir o model Reply para permitir saber qual thread está associdado.

```Python
class Reply(models.Model):

    thread = models.ForeignKey(
        Thread, verbose_name='Tópico', related_name='replies'
        )
    # omitido código sem alteração
```

Criar e executar as migrates da alteração realizada.

```Shell
python manage.py makemigrations
python manage.py migrate
```
Em seguida acessar a interface de admin do Django e cadastrar alguns tópicos para avaliar a tela de apresentação em http://localhost:3000/forum


## 79. Listagem dos Tópicos 2

### Objetivos

* Utilizando a ListView para listar Tópicos. Organizando a listagem de tags, paginação e demais links de navegação.

### Etapas

Na página `base.html` colocar um link para acessar o forum.

```Django
<div class="pure-menu pure-menu-open pure-menu-fixed pure-menu-horizontal">
    <a class="pure-menu-heading" href="{% url 'core:home' %}">SIMPLE MOOC</a>
    <ul>
        <li class="pure-menu-selected"><a href="{% url 'core:home' %}">Início</a></li>
        <li><a href="{% url 'courses:index' %}">Cursos</a></li>
        <li><a href="{% url 'forum:index' %}">Fórum</a></li>
        <!-- Omitido código sem alteração -->
    </ul>
</div>
```

No arquivo `views.py`, adicionar mais recursos na viw ForumView para retormar mais dados de contexto, neste caso todas as tags utilizadas.

```Python
class ForumView(ListView):
    # Omitido código sem alteração

    def get_context_data(self, **kwargs):
        context = super(ForumView, self).get_context_data(**kwargs)
        context["tags"] = Thread.tags.all()
        return context
```

Para organizar paginação, o Django dispõe da classe (Pagination)[https://docs.djangoproject.com/en/1.11/topics/pagination/] que pode paginar qualquer coisa que seja um iterável. Alterar no arquivo `index.html`.

```Django
<div class="pure-menu pure-menu-open">
    <ul>
        <!-- Omitido código sem alteração -->
        <li class="pure-menu-heading">Tags</li>
        <li>
            {% for tag in tags %}
                <a href="#" class="tags">
                    <i class="fa fa-tag"></i>
                    {{ tag }}
                </a>
            {% endfor %}
        </li>
    </ul>
</div>
<div class="inner">
    <!-- Omitido código sem alteração -->
    <ul class="pagination pagination-centered">
        {% if page_obj.has_previous %}
            <li>
                <a href="?page={{ page_obj.previous_page_number }}" title="">Anterior</a>
            </li>
        {% endif %}
        {% for page in  paginator.page_range %}
            <li>
                <a href="?page={{ page }}" title="">{{ page }}</a>
            </li>
        {% endfor %}
        {% if page_obj.has_next %}
            <li>
                <a href="?page={{ page_obj.next_page_number }}" title="">Próxima</a>
            </li>
        {% endif %}
    </ul>
</div>
```

Atualização em `style.css` para os links da paginação.

```CSS
/* Omitido código sem alteração */
.pure-menu li a.tags {
    display: inline-block;
}
.pagination {
  height: 36px;
  margin: 18px 0;
}

.pagination ul {
  display: inline-block;
  *display: inline;
  margin-bottom: 0;
  margin-left: 0;
  -webkit-border-radius: 3px;
     -moz-border-radius: 3px;
          border-radius: 3px;
  *zoom: 1;
  -webkit-box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
     -moz-box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
          box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.pagination li {
  display: inline;
}

.pagination a {
  float: left;
  padding: 0 14px;
  line-height: 34px;
  text-decoration: none;
  border: 1px solid #ddd;
  border-left-width: 0;
}

.pagination a:hover {
  text-decoration: none;
}

.pagination a:hover,
.pagination .active a {
  background-color: #f5f5f5;
}

.pagination .active a {
  color: #999999;
  cursor: default;
}

.pagination .disabled span,
.pagination .disabled a,
.pagination .disabled a:hover {
  color: #999999;
  cursor: default;
  background-color: transparent;
}

.pagination li:first-child a {
  border-left-width: 1px;
  -webkit-border-radius: 3px 0 0 3px;
     -moz-border-radius: 3px 0 0 3px;
          border-radius: 3px 0 0 3px;
}

.pagination li:last-child a {
  -webkit-border-radius: 0 3px 3px 0;
     -moz-border-radius: 0 3px 3px 0;
          border-radius: 0 3px 3px 0;
}

.pagination-centered {
  text-align: center;
}

.pagination-right {
  text-align: right;
}

.clear {
  clear: both;
  content: " ";
}

.text-right {
  text-align: right;
}
.text-left {
  text-align: left;
}
```