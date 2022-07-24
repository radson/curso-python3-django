## Aula 03 - Ambiente virtual

Criar ambiente virtual

```Shell
virtualenv venv -p python3
```

Para ativar o ambiente:

```Shell
$ source venv/bin/activate
```

Atualizando pacotes

```Shell
pip install -U pip wheel setuptools
```

Pacotes extra para melhor gestão da qualidade do código

```Shell
$ pip install flake8 mypy autopep8
```

Para desativar

```Shell
$ deactivate
```

## Aula 04 - Configurando o Django

```Shell
$ source venv/bin/activate
$ cd src
$ pip install django==1.11.29 #Ultima release, sem suporte desde 2020
$ django-admin startproject simplemooc
$ python manage.py runserver
```

## Aula 05 - Configurando o banco de dados

Será utilizado o sqlite3 pois o Django já possui suporte. No arquivo settings.py deve estar assim:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```

Alterar Language code

```python
LANGUAGE_CODE = 'pt-br'
```

Com o venv ativado, realizar a sincronização dos models com o banco de dados. 
 > No curso cita o 'syncdb', mas nas versòes mais atuais o comando é o 'migrate'. o syncdb também já cria o superuser. Nesta versão será executado em um comando a adicional ao curso.

 As tabelas sincronizadas estão relacionada as apps do Django: admin, auth, contenttypes, sessions

```Shell
$ python manage.py migrate
$ python manage.py createsuperuser
```
Agora criar a primeira aplicação dentro do projeto

```Shell
$ mkdir simplemooc/core
$ python manage.py startapp core simplemooc/core
```

Nos settings adicionar o novo app na lista de apps:

```python
INSTALLED_APPS = [
    'simplemooc.core',
]
```

No arquivo urls.py adicionar uma rota para o novo app

```python
from .core import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
]
```

No arquivo core/views.py adicionar a view referenciada no urls

```python
from django.http import HttpResponse

def home(request):
    return HttpResponse('Hello world!')

```

## Aula 06 - Introdução aos Templates

[Doc oficial do Django 1.11](https://docs.djangoproject.com/en/1.11/topics/templates/)

## Aula 07 - Primeiro Template

Executar o shell do projeto para realizar alguns testes com templates

```Shell
$ python manage.py shell
```

O shell irá carregar todas as configurações do Django o do projeto. Neste shell serão importadas as classes Template e Context. Em seguida instanciado um template que faz referencia a uma variável usuário e será instanciado um contexto criando a variável usuario com um valor.

```python
from django.template import Template, Context
template = Template("Bem vindo: {{ usuario }}")
context = Context({"usuario": "Radson"})
print(template.render(context))
```

Uma modificação para exemplificar, usando o modificador lower

```python
template = Template("Bem vindo: {{ usuario|lower }}")
print(template.render(context))
```

Opcionalmente pode-se instalar o shell iterativo ipython

```Shell
$ pip install ipython
```

Próxima etapa é criar a estrutura para os templates da app core. O Django reconhece o diretório 'template' dentro do diretório de cada app. Criar também o arquivo do primeiro template 'home.html'

```Shell
$ mkdir simplemooc/core/templates
$ > simplemooc/core/templates/home.html
```

Adicionar o conteúdo (ainda sem as tags HTML)

```Django
Simple MOOC
Usuario: {{ usuario }}
```

Alterar a view home chamando o shortcut render passando como parâmetro o request, o nome do template e um contexto (dicionário)

```python
def home(request):
    return render(request, 'home.html', {'usuario': 'Radson'})
```

## 08. Template base

Será criada uma página completa que será base do projeto. Para CSS será usado os módulos [Pure.css](https://purecss.io/)
> Para manter compatibilidade com o css personalizado do curso será mantido a mesma versão da época e não a mais atual.

No arquivo home.html criado na aula anterior será adicionado o conteúdo do arquivo base.html previamente já elaborado para o curso. Para o CSS apontar para o CDN do Pure.css e um arquivo adicional 'style.css' com a tag 'static' que contem um CSS personalizado para a aplicação.

```Django
{% load static %}
<link rel="stylesheet" href="http://yui.yahooapis.com/pure/0.3.0/pure-min.css">
<link rel="stylesheet" href="{% static 'css/styles.css' %}" />
```

A tag static determina urls específicas configuradas no settings.py que podem apontar para caminhos (ou servidores de conteúdo externo ao controle do Django), onde ficam os arquivos estáticos. Para este curso foi considerado o uso de um static para cada app. O conteúdo do arquivo style.css também já foi feito para o curso. 

```Shell
$ mkdir -p simplemooc/core/static/css
$ > simplemooc/core/static/css/style.css
```
## 09. Página de contato

Entender um pouco mais sobre views e urls criando uma página de contato.

No arquivo ```core/views.py``` adicionar uma novo método

```python
def contact(request):
    return render(request, 'contact.html')
```

No arquivode urls, adicionar a nova URL:

```python
url(r'^contato/$', views.contact, name='contact'),
```

Criar o novo arquivo de template em ```core/templates/contact.html``` com o conteúdo da nova página. O autor usou o mesmo conteúdo da 'home.html' alterando apenas a parte do conteúdo. Na próxima aula será utilizado o conceito de herança de templates para evitar repetição de código nos templates.

