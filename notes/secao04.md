# Seção 4: Sistema de Usuários

## 32. Introdução a Usuário

### Objetivos

* Conhecendo o pacote contrib.auth do Django para gerenciamento de usuários.

### Etapas

* Usar o mecanismos padrão de usuários do Django e extender o model User para as necessidades do curso.
* Para as próximas etapas, considerar o fonte do [auth.forms](https://github.com/django/django/blob/1.11.29/django/contrib/auth/forms.py) no github do projeto Django.

## 33. View de Login

### Objetivos

* Criar uma view para fazer login

### Etapas

Será utilizado o pacote contrib.auth do Django para fornecer o form e view de login.

Na raiz do projeto, adicionar novo app ```accounts``` para gerenciamento de autenticação de usuários:

```Shell
mkdir simplemooc/accounts
python manage.py startapp accounts simplemooc/accounts
```

No ```settings.py``` adicinar a nova app instalada:

```Python
INSTALLED_APPS = [
    # omitido código sem alteração
    'simplemooc.accounts',
]
```

No ```urls.py``` do projeto adicionar uma rota ```conta/``` apontando para ```simplemooc.accounts.urls```

```Python
urlpatterns = [
     # omitido código sem alteração
    url(r'^conta/', include('simplemooc.accounts.urls', namespace='accounts')),
]
```

Adicionar o arquivo ```accounts/urls.py``` com as rotas do app accounts.

```Python
from django.conf.urls import url
from django.contrib.auth import views as login_views

urlpatterns = [
    # Recebe dicionário com parametros nomeados, substituindo o template padrão do Django pelo customizado.
    url(r'^entrar/$', login_views.login, {'template_name': 'accounts/login.html'}, name='login'),
]
```

No  ```base.html``` adicionar no link apontando para url da para página de login

```Html
<ul>
    <li class="pure-menu-selected"><a href="{% url 'core:home' %}">Início</a></li>
    <!-- omitido código sem alteração -->
    <li><a href="{% url 'accounts:login' %}">Entrar</a></li>
</ul>
```

## 34. Template de Login

### Objetivos

* Criar um template para fazer login

### Etapas

No app ```accounts``` adicionar a estrutura de templates onde deverá ser criado o template ```login.html```.

```SHell
mkdir -p simplemooc/accounts/templates/accounts
> simplemooc/accounts/templates/accounts/login.html
```

O arquivo ```login.html``` irá utilizar o ```form``` do pacote ```auth``` do Django e deve ter o seguinte conteúdo:

```Jinja
{% extends 'base.html' %}

{% block content %}
<div class="pure-g-r content-ribbon">
    <div class="pure-u-1">
        <h2>Informe seus dados de cadastro</h2>
        <form action="" class="pure-form pure-form-aligned" method="post">
            {% csrf_token %}
            <fieldset>
                {{ form.non_field_errors }}

                {% for field in form %}
                    <div class="pure-control-group">
                        {{ field.label_tag }}
                        {{ field }}
                        {{ field.erros }}
                    </div>
                {% endfor %}

                <div class="pure-controls">
                    <button type="submit" class="pure-button pure-button-primary">Entrar
                    </button>
                </div>
            </fieldset>
            <p>
                Não é cadastrado? <a href="" title="">Cadastre-se</a><br>
                Esqueceu a senha? <a href="" title="">Nova Senha</a><br>
            </p>
        </form>
    </div>
</div>

{% endblock content %}
```

No final do arquivo ```settings.py``` do projeto, devem ser adicionadas rotas para referentes à ação de Login e Logout que são mapeadas no pacote auth do Django.

```Python
# Auth
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'core:home'
LOGOUT_URL = 'accounts:logout'
```

## 35. Form de Cadastro

### Objetivos

* Criar um form para cadastro do usuário com os recursos fornecidos pelo Django

### Etapas

No app ```accounts``` adicionar a estrutura de templates onde deverá ser criado o template ```register.html```.

```Shell
> simplemooc/accounts/templates/accounts/register.html
```

O arquivo ```register.html``` irá utilizar o ```form``` do pacote ```auth``` do Django e deve ter o seguinte conteúdo:

```Jinja
{% extends 'base.html' %}

{% block content %}
<div class="pure-g-r content-ribbon">
    <div class="pure-u-1">
        <h2>Informe seus dados</h2>
        <form action="" class="pure-form pure-form-aligned" method="post">
            {% csrf_token %}
            <fieldset>
                {{ form.non_field_errors }}

                {% for field in form %}
                    <div class="pure-control-group">
                        {{ field.label_tag }}
                        {{ field }}
                        {{ field.erros }}
                    </div>
                {% endfor %}

                <div class="pure-controls">
                    <button type="submit" class="pure-button pure-button-primary">
                        Cadastrar
                    </button>
                </div>
            </fieldset>
        </form>
    </div>
</div>

{% endblock content %}
```

No arquivo ```login.html``` adicionar o link que irá apontar para a rota de cadastro.

```Html
<!-- omitido código sem alteração -->
<p>
    Não é cadastrado? <a href="{% url 'accounts:register' %}" title="">Cadastre-se</a><br>
</p>
```

No arquivo  ```urls.py``` do app Accounts, adicionar nova rota para a view que será criada.

```Python
from . import views

urlpatterns = [
    # omitido código sem alteração
    url(r'^cadastre-se/$', views.register, name='register'),
]
```

Por fim, o arquivo de views do app Accounts deve conter a view ```register```, que irá usar o método ```UserCreationForm``` do pacote ```forms``` do Django. Será realizado o redirecionamento quando o login for válido, conforme definido no ```settings.py```. O conteúdo ficará:

```Python
from django.shortcuts import render, redirect
from django.conf import settings

from django.contrib.auth.forms import UserCreationForm

def register(request):
    template_name = 'accounts/register.html'

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(settings.LOGIN_URL)
    else:
        form = UserCreationForm()

    context = {
        'form': form
    }

    return render(request, template_name, context)
```

## 36. Custom Form de Cadastro

### Objetivos

* Customizar o form de cadastro para incluir o campo e-mail.

### Etapas

No app ```accounts``` adicionar ```forms.py``` que irá conter a definição do formulário personalizado com campo de e-mail herdendo de ```UserCreationForm```.

```Shell
> simplemooc/accounts/templates/accounts/register.html
```
 O conteúdo do ```forms.py``` conterá uma classe ```RegisterForm``` declarando o campo ```email``` e um método ```save``` que sobrescreve o metodo do objeto herdado.

```Python
from django import forms
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    email = forms.EmailField(label='E-mail')

    # Metodo save para substituir o save do UserCreationForm
    def save(self, commit=True):
        #Passando commit False o save retorna o objeto user e não salva no banco
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user
```

Na view, altera-se o import do ```UserCreationForm``` para o recem criado ```RegisterForm```.

```Python
# omitido código sem alteração ...
from .forms import RegisterForm

def register(request):
    # ...

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        # ...
    else:
        form = RegisterForm()
```

## 37. E-mail Único no Cadastro

### Objetivos

* Ajustar para que o campo e-mail seja obrigatório e único no banco de dados.

### Etapas

Implementar um método ```clean_email``` inspirado no ```clean_username``` que o form do pacote auth possui. O Django implementa o método iniciando com ```clean_``` concatenado com o nome do campo para realizar validações ou outras alterações necessárias na informaçõa do campo.

No ```forms.py``` do app Accounts, adicionar o método referido.

```Python
# omitido código sem alteração ...
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
# omitido código sem alteração ...

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Já existe usuário com este e-mail')

        return email
```

## 38. View de Logout

### Objetivos

* Implementar uma view de logout aproveitando os recursos disponíveis no pacote auth.
* Implementar o auto login após o cadastro do usuário

### Etapas

No ```urls.py``` da app Account, adicionar nova rota para logout. No dicionário que a função logout do pacote auth recebe, passar o redirecionamento que deverá ser a home do site. 

```Python
urlpatterns = [
    # omitido código sem alteração ...
    url(r'^sair/$', login_views.logout, {'next_page': 'core:home'}, name='logout'),
]
```

Na view do app Account importar os métodos ```authenticate``` e ```login``` que irão realizar a autenticação do usuário criado e o login colocando na variável de sessão as informações do user logado.

```Python
# omitido código sem alteração ...
from django.contrib.auth import authenticate, login

def register(request):
    # omitido código sem alteração ...
        if form.is_valid():
            user = form.save()
            user = authenticate(
                username=user.username, password=form.cleaned_data['password1']
            )
            login(request, user)

            return redirect('core:home')
```

No arquivo ```base.html``` ajustar o menu de links para verificar se o user está logado e oferecer a opção adequada Entrar ou Sair.

```Django
<!-- omitido código sem alteração -->
 <li><a href="{% url 'core:contact' %}">Contato</a></li>

{% if user.is_authenticated %}
    <li><a href="{% url 'accounts:logout' %}">Sair</a></li>
{% else %}
    <li><a href="{% url 'accounts:login' %}">Entrar</a></li>
{% endif %}
```

## 39. Painel do Usuário

### Objetivos

* Criar uma área para gerenciar os cursos cadastrados, alterar senha do usuário, uma tela do seu perfil.

### Etapas

Definição do escopo do perfil do usuário:

* Poder alterar senha
* Poder se inscrever em um curso (apenas o admin poderá criar novos cursos)
* Navegar nos cursos inscritos


## 40. Template do Painel do Usuário

### Objetivos

* Criar o template do painel do usuário

### Etapas

Adicionar nova rota padrão na app Accounts que será o index do usuário

```Python
urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
    # omitido código sem alteração ...
]
```

Na app Accounts adicionar o template ```accounts\templates\accounts\dashboard.html```. Neste template a variável ```user``` é utilizada para acessar informações sobre o usuário logado.

```Django
{% extends 'base.html' %}

{% block content %}
<div class="pure-g-r content-ribbon">
    <div class="pure-u-1-3">
        <h2>Meu painel</h2>
        <div class="pure-menu pure-menu-open">
            <a href="" class="pure-menu-heading"></a>
            <ul>
                <li class="pure-menu-heading">Meus Cursos</li>
                <li><a href="#">Curso 1</a></li>
                <li class="pure-menu-heading">Minha Conta</li>
                <li><a href="#">Editar Conta</a></li>
                <li><a href="#">Editar Senha</a></li>
            </ul>
        </div>
    </div>
    <div class="pure-u-2-3">
        <div class="inner">
            <p><strong>Usuário</strong>: {{ user }}</p>
            <p><strong>E-mail</strong>: {{ user.email }}</p>
        </div>
    </div>
</div>

{% endblock content %}
```

No ```base.html``` adicionar novo link para que o usuário autenticado consiga entrar no Dashboard

```Django
{% if user.is_authenticated %}
    <li><a href="{% url 'accounts:dashboard' %}">Painel</a></li>
    <li><a href="{% url 'accounts:logout' %}">Sair</a></li>
{% else %}
    <li><a href="{% url 'accounts:login' %}">Entrar</a></li>
{% endif %}
```

No arquivo de views, adicionar a view respectiva ao Dashboard. A view deverá utilizar o recurso chamado decorator do Django, o decorator ```login_required``` irá requisitar que o usuário esteja logado, conforme [documentação](https://docs.djangoproject.com/pt-br/1.11/_modules/django/contrib/auth/decorators/). Caso contrário, irá direcionar para a página de login e a URL após o login será a que aponta para a view que requisitou.

```Python
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    template_name = 'accounts/dashboard.html'
    return render(request, template_name)
```

## 41. View de Edição de Conta

### Objetivos

* Iniciar a implementação da view do Dashboar do usuário

### Etapas

Adicionar um breadcrumb no template ```dashboard.html``` substituindo a tag h2 com o título da página por um bloco content. Adicionar o mesmo bloco para os dados do usuário, desse modo será possível utilizar o recurso de herança da herança de template. Alterar a rota para o link *Editar Conta*.

```Django
<div class="pure-u-1-3">
    <ul class="breadcrumb">
        {% block breadcrum %}
            <li><a href="{% url 'accounts:dashboard' %}">Meu Painel</a></li>
        {% endblock breadcrum %}
    </ul>
    <!-- omitido código sem alteração -->
    <li><a href="{% url 'acounts:edit' %}">Editar Conta</a></li>
</div>
<div class="pure-u-2-3">
    <div class="inner">
        {% block dashboard-content %}
            <p><strong>Usuário</strong>: {{ user }}</p>
            <p><strong>E-mail</strong>: {{ user.email }}</p>
        {% endblock dashboard-content %}
    </div>
</div>
```

No views, adicionar respectiva view para editar a conta:

```Python
@login_required
def edit(request):
    template_name = 'accounts/edit.html'
    return render(request, template_name)
```

No arquivo de rotas ```urls.py``` adicionar a nota para editar o perfil

```Python
urlpatterns = [
    url(r'^editar/$', views.edit, name='edit'),
]
```