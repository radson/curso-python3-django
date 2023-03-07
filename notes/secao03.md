# Seção 3: Visão Externa dos Cursos

## 19. View de cursos

### Objetivos

* Criar uma página de listagem dos cursos

### Etapas

No arquivo  ```courses/views.py ``` definir a primeira view com o conteúdo:

```Python
def index(request):
    template_name = 'courses/index.html'
    return render(request, template_name)
```

Para que seja acessível, é necessário criar o arquivo de urls em ```courses/urls.py``` na app courses com o conteúdo

```Python
urlpatterns = [
    url(r'^$', views.index, name='index'),
]
```

No arquivo urls.py do projeto, adicionar o include das urls de courses

```Python
    url(r'^cursos/', include('simplemooc.courses.urls', namespace='courses')),
```

Criar o template para courses

```Shell
mkdir -p simplemooc/courses/templates/courses
> simplemooc/courses/templates/courses/index.html
```

O conteúdo do arquivo index.html deve extender do template base e definir um bloco de conteúdo que será substituído no base pelo conteúdo que será específico desta página. O conteúdo dinâmico será criado na próxima aula.

```Django
{% extends 'base.html' %}

{% block content %}

{% endblock content %}
```

## 20. Listagem dos Cursos

### Objetivos

* Criar uma página de listagem dos cursos trazendo as informações do banco de dados

### Etapas

* Na views do módulo course importar os models de curso e incrementar no método index a consulta ao model e um contexto a ser passado para o template com os registros retornados.

```Python
from .models import Course

def index(request):
    courses = Course.objects.all()
    template_name = 'courses/index.html'
    context = {
        'courses': courses
    }
    return render(request, template_name, context)
```

No template adicionar um laço for iterando nos registros passados pelo contexto e acessando as propriedades mapeadas no model

```Django
{% for course in courses  %}
    {{ course.name }}
    {{ course.description|linebreaks }}
{% endfor %}
```

## 21. Trabalhando com as imagens dos cursos

### Objetivos

* Incrementar o template utilizando mais recursos para exibir a página para o curso

### Etapas

* Adicionar imagem para o curso, utilizar uma imagem padrão quando não for fornecida uma.
* Imagem estática no caminho ```core/static/img/course-image.png```
* No arquivo ```index.html``` adicionar uma verificação, caso exista uma imagem setada pegar do model ou pegar a estática

```Django
{% load static %}

{% if course.image %}
    <img src="{{ course.image.url }}" alt="{{ course.name }}" />
{% else %}
    <img src="{% static 'img/course-image.png' %}" alt="{{ course.name }}" />
{% endif %}
```

* No caso haja arquivos de imagem inseridos via form, será necessário definir a estrutura para servir estes arquivos estáticos.
* No arquivo do projeto ```settings.py``` definir o caminho da URL para arquivos de mídia

```Python
MEDIA_URL = '/media/'
```

* No arquivo ```urls.py``` do projeto, inserir uma verificação para quando estiver em modo DEBUG incluir mais uma URL:

```Python
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

## 22. Página do curso

### Objetivos

* Criar a página de exibição do detalhe do curso

### Etapas

* No models incluir o campo ```about``` para a classe Courses que deverá ser um campo com uma descrição mais detalhada do curso.

```Python
class Course(models.Model):

    # ... declarações anteriores
    about = models.TextField("Sobre o curso", blank=True)
```

* Após modificar o model deve-se gerar e aplicar as migrations

```Shell
python manager.py makemigrations
python manager.py migrate
```

* No arquivo de urls da app courses, adicionar nova rota para página de detalhes do curso.

```Python
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<pk>\d+)/$', views.details, name='details')
]
```

* No arquivo de views, adicionar nova view como a seguir:

```Python
def details(request, pk):
    course = Course.objects.get(pk=pk)
    context = {
        'course': course
    }
    template_name = 'courses/details.html'

    return render(request, template_name, context)
```

* Criar o arquivo ```details.html``` no diretório de templates da app courses

## 23. Exibindo o curso

### Objetivos

* Realizar a exibição das informações do curso e tratamento de erros

### Etapas

* Alterar a view details, substituindo o uso do manager do objeto Course pelo atalho get

```Python
from django.shortcuts import get_object_or_404

def details(request, pk):
    course = get_object_or_404(Course, pk=pk)
    # ...
```

* No arquivo de template ```details.html``` declarar as propriedades que serão exibidas.

```Django
{% extends 'base.html' %}

{% block content %}

<div class="splash">
    <div class="pure-g-r">
        <div class="pure-u-1">
            <div class="l-box splash-text">
                <h1 class="splash-head">
                    {{ course }}
                </h1>
                <h2 class="splash-subhead">
                    {{ course.description }}
                </h2>
                <p>
                    <a href="#" class="pure-button primary-button">Inscreva-se</a>
                </p>
            </div>
        </div>
    </div>
</div>
<div class="pure-g-r content-ribbon">
    <div class="pure-u-2-3">
        <div class="l-box">
            <h4 class="content-subhead">Sobre o curso</h4>
            {{ course.about|linebreaks }}
        </div>
    </div>
    <div class="pure-u-1-3">
        <div class="l-box">
            {% if course.image %}
                <img src="{{ course.image.url }}" alt="{{ course.name }}" />
            {% else %}
                <img src="{% static 'img/course-image.png' %}" alt="{{ course.name }}" />
            {% endif %}
        </div>
    </div>
</div>

{% endblock content %}
```

O uso do [linebreak](https://docs.djangoproject.com/en/1.8/ref/templates/builtins/#linebreaks) serve para transformar as quebras de linha em HTML.