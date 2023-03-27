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

## 24. Usando Slug no Curso

### Objetivos

* Uso do Slug na url para acessar o curso em substituição do ID do registro no banco de dados.

### Etapas

* Mudar a rota anteriormente definida para uma expressão regular que recebe o parametro ```slug``` que aceita letras, hífen e underline.

```Python
urlpatterns = [
    # url(r'^(?P<pk>\d+)/$', views.details, name='details')
    url(r'^(?P<slug>[\w_-]+)/$', views.details, name='details')
]
```

* No arquivo de views, alterar para receber o parametro ```slug``` e passar para a consulta no banco de dados:

```Python
def details(request, slug):
    course = get_object_or_404(Course, slug=slug)
    context = {
        'course': course
    }
    template_name = 'courses/details.html'

    return render(request, template_name, context)
```

* Para testar acessar na url ```http://localhost:8000/cursos/slug``` onde a string ```slug``` deve ser igual ao cadastrado para o curso (usar do Django Admin para consultar)

* Para o melhor mapeamento das URLs o Django recomenda o uso do método ```get_absolute_url``` dentro do model para retornar a URL canonica de um objeto, mais detalhes na [documentação]:(https://docs.djangoproject.com/en/1.8/ref/models/instances/#get-absolute-url). Adicionalmente deve-se utilizar o decorator ```@model.permalink``` para o Django realizar o retorno da URL do objeto.

```Python
class Course(models.Model):
    # ...
    
    @models.permalink
    def get_absolute_url(self):
        return ("courses:details", (), {"slug": self.slug})
```

No arquivo ```index.html``` do template agora pode-se atualizar as propriedades href com a URL implementada

```Django
<a href="{{ course.get_absolute_url }}">
    {% if course.image %}
        <img src="{{ course.image.url }}" alt="{{ course.name }}" />
    {% else %}
        <img src="{% static 'img/course-image.png' %}" alt="{{ course.name }}" />
    {% endif %}
</a>
<!-- ... -->
<h4 class="content-subhead"><a href="{{ course.get_absolute_url }}" title="{{ course.name }}">{{ course.name }}</a></h4>
```

Essa é uma forma padronizada de trabalhar com URLs em aplicações Django, alguns aplicativos de terceiros esperam essa funcionalidade implementada, a exemplo da interface de administração do Django que mostra o botão *View on site* quando se está acessando a página de algum objeto que tem o ```get_absolute_url``` implementado.

## 25. Introdução do Django Form

### Objetivos

* Breve introdução sobre o sistema de formulários do Django.

### Etapas

* O Django possui uma engine que faz processamento, exibição do HTML e validação dos dados. Além disso há o recurso de arquivos de media para ser utilizado em campos personalizados.

## 26. Form de Contato do Curso

### Objetivos

* Criar um form para tirar dúvidas sobre o curso.

### Etapas

* Criar um arquivo ```forms.py``` na app de cursos. O form é uma classe que herda de django.forms.

```Python
from django import forms

class ContactCourse(forms.Form):
    name = forms.CharField(label='Nome', max_length=100)
    email = forms.EmailField(label='E-mail')
    message = forms.CharField(label='Mensagem/Duvida', widget=forms.Textarea)
```

Com o shell do Django é possível validar o uso dos forms

```Shell
./manage.py shell
```

No prompt de comandos interativo do Django executar os comandos:

```Python
from simplemooc.courses.forms import ContactCourse

form = ContactCourse()

print(form.as_p())
```

O método ```as_p()``` irá exibir os campos do form dentro de tags <p>

```Html
<p><label for="id_name">Nome:</label> <input type="text" name="name" maxlength="100" required id="id_name" /></p>
<p><label for="id_email">E-mail:</label> <input type="email" name="email" required id="id_email" /></p>
<p><label for="id_message">Mensagem/Duvida:</label> <textarea name="message" cols="40" rows="10" required id="id_message">
</textarea></p>
```

Criando um dicionário para submeter ao form e verificando se os dados são válidos

```Python
data = {'name': 'radson', 'email': 'radson@rass.tech'}

form = ContactCourse(data)

form.is_valid()

form.errors
```

O método ```is_valid()``` irá retornar  ```False``` e a propriedade ```errors``` irá retornar um dicionário dos essos para cada campo.

```Python
{'message': ['This field is required.']}
```

## 27. Form no Template

### Objetivos

* Implementar o form nos templates.

### Etapas

Na view do curso, método datails, inserir no contexto a classe ContactForm. Deverá ser verificado se o request é um GET ou POST para decidir se a classe ContactForm será instanciada vazia ou com os dados submetidos.

```Python
from .forms import ContactCourse

def details(request, slug):
    course = get_object_or_404(Course, slug=slug)

    if request.method == 'POST':
        form = ContactCourse(request.POST)
    else:
        form = ContactCourse()

    context = {
        'course': course,
        'form': form
    }
    template_name = 'courses/details.html'

    return render(request, template_name, context)
```

No template, adicionar o form usando a linguagem de template. Para este exemplo foi utilizada exibição customizada onde os campos podem ser trabalhados invidualmente, porém o Django fornece uma exibição padrão apenas especificando a variável recebida pelo contexto. 

```Django
<div class="pure-g-r content-ribbon" id="contato">
    <div class="pure-u-1">
        <h3>Tire sua dúvida sobre o Curso</h3>
        <form class="pure-form pure-form-aligned" method="POST">
            {% csrf_token %}
            <fieldset>
                {% for field  in form  %}
                    <div class="pure-control-group">
                        {{ field.label_tag }}
                        {{ field }}
                        {% if field.erros  %}
                            <ul class="errorlist">
                                {% for error  in field.erros %}
                                    <li>{{error}}</li>
                                {% endfor %}
                            </ul>
                        {% endif %}
                    </div>
                {% endfor %}
                <div class="pure-controls">
                    <button type="submit" class="pure-button pure-button-primary">Enviar</button>
                </div>
            </fieldset>
        </form>
    </div>
</div>
```

## 28. Submetendo o Form do Curso

### Objetivos

* Implementar o form na view.

### Etapas

No metodo details, será adicionada verificação se o form é válido com o método ```is_valid()```. Quando os dados são válidos, devem ser acessados apenas no dicionário ```cleaned_data``` que contem os dados validados e convertidos para tipos de dados do Python. Para facilitar o entendimento foi passada a variável de ambiente ```is_valid``` para ser exibida no template quando o form estiver válido e no console será impresso os dados já validados.

```Python
def details(request, slug):
    course = get_object_or_404(Course, slug=slug)
    context = {}

    if request.method == 'POST':
        form = ContactCourse(request.POST)
        if form.is_valid():
            context['is_valid'] = True
            print(form.cleaned_data['name'])
            print(form.cleaned_data['message'])
            form = ContactCourse()
    else:
        form = ContactCourse()

    context['course'] = course
    context['form'] = form

    # restante do código já implementado
```

Exibindo a váriável de contexto para quando o form é válido.

```Django
<h3>Tire sua dúvida sobre o Curso</h3>
{% if is_valid %}
    <p>Formulário enviado com sucesso</p>
{% endif %}
```