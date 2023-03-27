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

## 29. Introdução ao Envio de E-mail

### Objetivos

* Introdução ao sistema de envio de email do Django

### Etapas

O Django provê o mecanismo de e-mail backend para fazer um processamento/armazenamento do e-mail antes do envio. O mais comum é o uso de um SMTP para envio de e-mail, porém para esse exemplo inicialmente será usado o backend ```console```, que deverá ser configurado no arquivo ```settings.py```.

```Python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

No shell pode ser feito o seguinte teste

```Python
from django.core.mail import send_mail

send_mail('Assunto', 'Mensagem', 'sender@localhosts.local', ['receiver1@localhosts.local', 'receiver2@localhosts.local'])
```

O resultado será como a seguir. Com o backend console o e-mail em vez de ser enviado é apenas impresso no console.

```
Content-Type: text/plain; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Subject: Assunto
From: sender@localhosts.local
To: receiver1@localhosts.local, receiver2@localhosts.local
Date: Mon, 27 Mar 2023 14:31:06 -0000
Message-ID: <20230327143106.15905.26092@dellg7>

Mensagem
-------------------------------------------------------------------------------
```

## 30. Integrando o envio de e-mail com Form

### Objetivos

* Implementando o envio de e-mail no form de contato

### Etapas

No arquivo ```settings.py``` devem ser configuradas as demais variáveis para envio de e-mail via SMTP. Adicionalmente foi criada uma variável CONTACT_EMAIL que deverá receber os emails enviados.

```Python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = 'Contato <contato@simplemooc.com>'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'simplemooc@gmail.com'
EMAIL_HOST_PASSWORD = 'senha'

CONTACT_EMAIL = 'contato@simplemooc.com'
```

No arquivo   ```forms.py``` é onde deve ficar a lógica de envio de e-mails (uma boa prática para que as views cuidem apenas da exibição). Para isso adicionar o método ```send_mail(self, course)``` que recebe um curso como parâmetro. Deve-se importar o método ```send_mail``` e para acessa as settings do projeto importar ```settings```.

```Python
from django.core.mail import send_mail
from django.conf import settings

class ContactCourse(forms.Form):
    # omitido código do form

    def send_mail(self, course):
        subject = '[%s] Contato' % course
        message = 'Nome: %(name)s;Email: %(email)s;%(message)s'
        context = {
            'name': self.cleaned_data['name'],
            'email': self.cleaned_data['email'],
            'message': self.cleaned_data['message'],
        }
        message = message % context

        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [settings.CONTACT_EMAIL])
```

Na view, após validação do form, deve-se invocar o método implementado passando o curso

```Python
def details(request, slug):
    # omitido código inalterado

    if request.method == 'POST':
        form = ContactCourse(request.POST)
        if form.is_valid():
            context['is_valid'] = True
            form.send_mail(course)
            form = ContactCourse()
    else:
        form = ContactCourse()

    # omitido código inalterado
```

## 31. Organizando o envio de E-mail com Templates

### Objetivos

* Criar um template de email para centralizar o envio de email na app.

### Etapas

Na app core criar um arquivo ```mail.py``` com o seguinte conteúdo:

```Python
from django.template.loader import render_to_string
from django.template.defaultfilters import striptags
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


def send_mail_template(subject, template_name, context, recipient_list,
                       from_email=settings.DEFAULT_FROM_EMAIL, fail_silently=False):

    message_html = render_to_string(template_name, context)
    message_text = striptags(message_html)

    email = EmailMultiAlternatives(
        subject=subject, body=message_text, from_email=from_email,
        to=recipient_list
    )

    email.attach_alternative(message_html, "text/html")
    email.send(fail_silently=fail_silently)
```

* ```render_to_string```: Faz a renderização de um template em formato string
* ```striptags```: Remove as tags HTML da string gerada
* ```EmailMultiAlternatives```: Uma classe que cria um e-mail com conteúdo alternativo (padrão em texto, alternativo em HTML)

Criar um novo template para o e-mail de contato em ```courses/templates/courses/contact_email.html``` com o conteúdo:

```Django
<p><strong>Nome</strong>: {{ name }}</p>
<p><strong>E-mail</strong>: {{ email }}</p>
{{ message | linebreaks}}
```

No arquivo ```forms.py``` atualizar o método ```send_mail```, onde é removida a variável da mensagem e é adicionado o template criado.

```Python
from simplemooc.core.mail import send_mail_template

class ContactCourse(forms.Form):
    # omitido código inalterado

    def send_mail(self, course):
        subject = '[%s] Contato' % course
        context = {
            'name': self.cleaned_data['name'],
            'email': self.cleaned_data['email'],
            'message': self.cleaned_data['message'],
        }

        template_name = 'courses/contact_email.html'

        send_mail_template(subject, template_name, context,
                           [settings.CONTACT_EMAIL])
```