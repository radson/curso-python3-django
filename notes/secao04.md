# Seção 4: Sistema de Usuários

## 32. Introdução a Usuário

### Objetivos

* Conhecendo o pacote contrib.auth do Django para gerenciamento de usuários.

### Etapas

* Usar o mecanismos padrão de usuários do Django e extender o model User para as necessidades do curso.

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