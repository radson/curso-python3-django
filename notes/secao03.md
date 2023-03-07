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
    <img src="{{ course.image.url }}" alt="{{ course.name }}">
{% else %}
    <img src="{% static 'img/course-image.png' %}" alt="{{ course.name }}/>
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