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