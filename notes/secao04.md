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