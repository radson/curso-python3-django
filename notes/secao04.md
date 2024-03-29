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
                        {{ field.errors }}
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
                        {{ field.errors }}
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
    <li><a href="{% url 'accounts:edit' %}">Editar Conta</a></li>
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

## 42. Formulário para Edição de Conta

### Objetivos

* Criar um form para editar os dados da conta do usuário

### Etapas

Criar um novo template  ```accounts/edit.html``` que vai herdar os blocos ```breadcrumb``` e ```dashboard_content``` do template ```dashboard.html```

```Django
{% extends 'accounts/dashboard.html' %}


{% block breadcrumb %}
    {% comment "" %}Mantem o conteúdo do bloco que foi herdado e adicina o conteúdo a seguir.{% endcomment %}
    {{ block.super }}
    <li>/</li>
    <li><a href="{% url 'accounts:edit' %}">Editar Conta</a></li>
{% endblock breadcrumb %}

{% block dashboard_content %}
<form class="pure-form pure-form-stacked">
    {% csrf_token %}
    <fieldset>
        {{ form.non_field_errors }}
        {% for field in form %}
            <div class="pure-control-group">
                {{ field.label_tag }}
                {{ field }}
                {{ field.errors }}
            </div>
        {% endfor %}

        <div class="pure-controls">
            <button type="submit" class="pure-button pure-button-primary">Enviar
            </button>
        </div>
    </fieldset>
</form>
{% endblock dashboard_content %}
```

Em ```forms.py``` ciar a classe ```EditAccountForm``` que irá criar os campos do formulário a partir dos campos do model ```User```.

```Python
class EditAccountForm(forms.ModelForm):

    def clean_email(self):
        email = self.cleaned_data['email']
        queryset = User.objects.filter(email=email).exclude(pk=self.instance.pk)
        if queryset.exists():
            raise forms.ValidationError('Já existe usuário com este e-mail')

        return email

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
```

No ```views.py``` editar a view ```edit``` que implementa a passagem do form via parâmetro para o template.

```Python
# omitido código sem alteração
from .forms import RegisterForm, EditAccountForm

@login_required
def edit(request):
    template_name = 'accounts/edit.html'
    form = EditAccountForm()
    context = {}
    context['form'] = form

    return render(request, template_name, context)
```

## 43. Confirmação de Edição de Conta

### Objetivos

* Implementar uma confirmação de edição de conta

### Etapas

No arquivo ```views.py``` alterar a view ```edit``` para controlar quando o request for do tipo ```POST```.

```Python
# omitido código sem alteração
@login_required
def edit(request):
    template_name = 'accounts/edit.html'
    context = {}

    if request.method == 'POST':
        form = EditAccountForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            form = EditAccountForm(instance=request.user)
            context['success'] = True
    else:
        form = EditAccountForm(instance=request.user)

    context['form'] = form

    return render(request, template_name, context)
```

No template ```edit.html``` incluir uma verificação de a variável ```success``` está no contexto, indicando que os dados foram persistidos com sucesso.

```Django
<form class="pure-form pure-form-stacked" method="post">
    {% csrf_token %}
    {% if success %}
        <p>Os dados foram alterados com sucesso.</p>
    {% endif %}
    <!-- omitido código sem alteração -->
</form>
```

## 44. Edição de Senha

### Objetivos

* Permitir ao usuário alterar sua senha.

### Etapas

Adicionar uma view ```edit_password``` que irá fazer uso do form que o Django disponibiliza ```PasswordChangeForm``` para alterar senha do usuário. O form recebe os dados do POST e o usuário que está logado.

```Python
from django.contrib.auth.forms import PasswordChangeForm
# omitido código sem alteração

@login_required
def edit_password(request):
    template_name = 'accounts/edit_password.html'
    context = {}

    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            context['success'] = True
    else:
        form = PasswordChangeForm(user=request.user)

    context['form'] = form

    return render(request, template_name, context)
```

Deve ser criado um template novo para tratar da senha, com nome ```edit_password.html``` pois é como funciona o PasswordChangeForm. Ele será com a mesma estrutura do template ```edit.html``` com algumas alterações nos labels.

```Django
{% block breadcrumb %}
    <!-- omitido código sem alteração -->
    <li><a href="{% url 'accounts:edit_password' %}">Editar Senha</a></li>
{% endblock breadcrumb %}

{% block dashboard_content %}
    <form class="pure-form pure-form-stacked" method="post">
        {% csrf_token %}
        {% if success %}
            <p>Senha alterada com sucesso.</p>
        {% endif %}
        <fieldset>
            <!-- omitido código sem alteração -->
            <div class="pure-controls">
                <button type="submit" class="pure-button pure-button-primary">Alterar Senha
                </button>
            </div>
        </fieldset>
    </form>
{% endblock dashboard_content %}
```

No arquivo ```urls.py``` adicionar a rota respectiva para alterar senha

```Python
urlpatterns = [
    # omitido código sem alteração
    url(r'^editar-senha/$', views.edit_password, name='edit_password'),
]
```

No template ```dashboard.html``` alterar a url do link para alterar senha

```Django
<ul>
    <!-- omitido código sem alteração -->
    <li><a href="{% url 'accounts:edit_password' %}">Editar Senha</a></li>
</ul>
```

## 45. Introdução ao Custom User

### Objetivos

* Explicação do usuário extendendo os campos do model User do Django.

### Etapas

Mais detalhes na documentação [Estendendo o modelo Usuário existente](https://docs.djangoproject.com/pt-br/1.11/topics/auth/customizing/#extending-the-existing-user-model)

## 46. Custom User Model

### Objetivos

* Criar um model customizado estendendo o model User do Django.

### Etapas

Na app Accounts, no arquivo ```models.py``` adicionar o model ```User``` com os campos personalizados que será utilizado no lugar do ```User``` padrão do Django para esta aplicação. Serão realizados os seguintes imports:

* AbstractBaseUser: Já tem a lógica para alterar senha. Traz os campos senha e lastlogin.
* PermissionMixin: Traz mecanismos de permissões e buscas
* UserManager: Implementa funcoes de gerenciamento de usuário

```Python
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
UserManager)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('Nome de Usuário', max_length=30, unique=True)
    email = models.EmailField('E-mail', unique=True)
    name = models.CharField('Nome', max_length=100, blank=True)
    is_active = models.BooleanField('Está ativo?', blank=True, default=True)
    is_staff = models.BooleanField('É da equipe?', blank=True, default=False)
    date_joined = models.DateTimeField('Data de entrada', auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.name or self.username

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return str(self)

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
```

No ```settings.py```, adicionar ao final do arquivo a variável ```AUTH_USER_MODEL``` que indica ao Django qual será o model padrão para gerenciamento de usuário.

```Python
# omitido código sem alteração
AUTH_USER_MODEL= 'accounts.User'
```

## 47. Ajustes na aplicação para o Custom User

### Objetivos

* Realizar os ajustes na aplicação para ficar compatível com o novo modelo de models.

### Etapas

No ```models.py``` do app Accounts, modificar o model ```User``` para fazer uso do mesmo validator que o Django utiliza para o username.

```Python
import re
from django.core import validators
# omitido código sem alteração

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        'Nome de Usuário', max_length=30, unique=True,
        validators=[validators.RegexValidator(re.compile('^[\w.@+-]+$'), 
        'O nome de usuário só pode conter letras, números ou os caracteres @/./+/-/_',
        'invalid')]
    )
    # omitido código sem alteração
```

Em ```forms.py``` será necessário revisar o código para identificar o que ainda continua compatível e o precisa ser refeito de acordo com o novo model de usuários. Na [documentação](https://docs.djangoproject.com/pt-br/1.11/topics/auth/customizing/#custom-users-and-the-built-in-auth-forms) do Django explica quais forms precisam ser reescritos quando um model customizado é utilizado. O ```UserCreationForm``` não é compatível com o model de usuário customizado e deve ser removido, bem como a função ```clean_email``` pois agora o campo do model está configurado como único. Adicionar também a class  ```Meta``` informando os campos utilizados.

```Python
 # omitido código sem alteração
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterForm(forms.ModelForm):

    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(label='COnfirmação de Senha', widget=forms.PasswordInput)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('A confirmação não está correta')
        
        return password2

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        # omitido código sem alteração

    class Meta:
        model = User
        fields = ['username', 'email']

class EditAccountForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'name']
```

Apagar o arquivo sqlite e gerar novamente rodando o migrate. Será possível notar que não gerada a tabela ```auth_user``` e no seu lugar será a ```accounts_user```

```Shell
rm db.sqlite3
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

## 48. Introdução a Criação de Nova Senha

### Objetivos

* Fluxo para redefinir a senha. 
* Criar um model para gerenciamento de uma chave única randomica para recuperação de senha.

### Etapas

Em ```models.py``` adicionar um novo model  ```PasswordReset``` para permitir gerenciar as solicitações de nova senha dos usuários. O model terá relação com o model de autenticação definidos no ```settings``` e não o padrão do Django. 

```Python
class PasswordReset(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Usuário',
        #related_name='resets'
    )

    key = models.CharField('Chave', max_length=100, unique=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    confirmed = models.BooleanField('Confirmado?', default=False, blank=True)

    class Meta:
        verbose_name = "Nova Senha"
        verbose_name_plural = "Novas Senhas"
        ordering = ['-created_at'] # Ordenaçao decrescente pela data.

    def __str__(self):
        return f'{0} em {1}'.format(self.user, self.created_at)
```

Em seguida realizar a migração no banco de dados.

```Shell
python manage.py makemigrations
python manage.py migrate
```

## 49. Gerando a chave única para o PasswordRest Model

### Objetivos

* Implementar mecanismo onde o usuário solicita mudar a senha em um formulário onde informa o e-mail, recebe um link com um token (key) 

### Etapas

Na app ```core``` criar um arquivo ```utils.py ```com funções para auxiliar a geração da senha.

```Python
import hashlib
import string
import random

def random_key(size=5):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for x in range(size))

def generate_hash_key(salt, random_str_size=5):
    random_str = random_key(random_str_size)
    text = random_str + salt
    return hashlib.sha224(text.enconde('utf-8')).hexdigest()
```

No model usar o recurso de ```related_name``` para que o model ```User``` possa acessar de forma reversa o model que tem relação via ForeignKey e saber os registros (quantos resets de senha) o user tem. Mais detalhes na [documentação](https://docs.djangoproject.com/en/1.11/ref/models/options/#default-related-name)

```Python
class PasswordReset(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Usuário',
        related_name='resets'
    )

    # omitido código sem alteração
```

## 50. Form para o PasswordRest

### Objetivos

* Adicionar o form do fluxo de solicitação de nova senha

### Etapas

Adicionar um nova classe no ```forms.py``` que irá exibir e validar o campo e-mail que será usado para recuperar a senha.

```Python
class PasswordResetForm(forms.Form):
    email = forms.EmailField(label='E-mail')

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email=email).exists():
            return email

        raise forms.ValidationError('Nenhum usuário encontrado com este e-mail')
```

Criar nova view ```password_reset``` em uma construção diferente das views anteriores com forms, onde o ```PasswordResetForm``` recebe como parametro o ```request.POST``` ou ```None```. Esta forma substitui as verificacões para saber se o ```request``` é GET ou POST. O Django aceita o None quando não houver dados no POST desse modo evitando a validação do form.

```Python
from django.contrib.auth import authenticate, login, get_user_model

from simplemooc.core.utils import generate_hash_key
from .forms import RegisterForm, EditAccountForm, PasswordResetForm
from .models import PasswordReset

User = get_user_model()

# omitido código sem alteração

def password_reset(request):
    template_name = 'accounts/password_reset.html'
    context = {}

    form = PasswordResetForm(request.POST or None)

    if form.is_valid():
        user = User.objects.get(email=form.cleaned_data['email'])
        key = generate_hash_key(user.username)
        reset = PasswordReset(key=key, user=user)
        reset.save()
        context['success'] = True
    
    context['form'] = form

    return render(request, template_name, context)
```

Criar um novo template em ```templates/accounts/password_reset.html```

```Django
{% extends 'base.html' %}

{% block content %}
<div class="pure-g-r content-ribbon">
    <div class="pure-u-1">
        {% if success %}
            <p>Você receberá um e-mail informando como gerar nova senha.</p>
        {% else %}
            <h2>Informe seu e-mail</h2>
            <form action="" class="pure-form pure-form-stacked" method="post">
                {% csrf_token %}
                <fieldset>
                    {{ form.non_field_errors }}
                    
                    {% for field in form %}
                        <div class="pure-control-group">
                            {{ field.label_tag }}
                            {{ field }}
                            {{ field.errors }}
                        </div>
                    {% endfor %}
                    
                    <div class="pure-controls">
                        <button type="submit" class="pure-button pure-button-primary">
                            Enviar e-mail
                        </button>
                    </div>
                </fieldset>
            </form>
        {% endif %}
    </div>
</div>

{% endblock content %}
```

Adicionar a nova rota em ```urls.py```.

```Python
urlpatterns = [
    # omitido código sem alteração
    url(r'^nova-senha/$', views.password_reset, name='password_reset'),
]
```

No arquivo ```login.html``` atualizar o link para o novo template.

```Html
<!-- omitido código sem alteração -->
Esqueceu a senha? <a href={% url 'accounts:password_reset' %} title="">Nova Senha</a><br>
```

## 51. Form para criar nova senha

### Objetivos

* Reorganização da lógica de criar nova senha

### Etapas

Mover lógica da view ```password_reset``` para dentro do de ```PasswordResetForm``` em ```forms.py``` e adicionar nova view ```password_reset_confirm``` que usará um form do Django para alterar senha.

```Python
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import SetPasswordForm

# omitido código sem alteração

def password_reset(request):
    template_name = 'accounts/password_reset.html'
    context = {}

    form = PasswordResetForm(request.POST or None)

    if form.is_valid():
        form.save()
        context['success'] = True
    
    context['form'] = form

    return render(request, template_name, context)

def password_reset_confirm(request, key):
    template_name = 'accounts/password_reset_confirm.html'
    context = {}
    reset = get_object_or_404(PasswordReset, key=key)
    form = SetPasswordForm(user=reset.user, data=request.POST or None)

    if form.is_valid():
        form.save()
        context['success'] = True
    
    context['form'] = form

    return render(request, template_name, context)
```

A lógica que saiu da view ```password_reset``` passa a ser o método ```save``` que irá enviar email para o user resetar a senha.

```Python
from simplemooc.core.utils import generate_hash_key
from simplemooc.core.mail import send_mail_template
from .models import PasswordReset

class PasswordResetForm(forms.Form):
    
    # omitido código sem alteração

    def save(self):
        user = User.objects.get(email=self.cleaned_data['email'])
        key = generate_hash_key(user.username)
        reset = PasswordReset(key=key, user=user)
        reset.save()
        template_name = 'accounts/password_reset_mail.html'
        subject = 'Criar nova senha no Simple Mooc'
        send_mail_template(subject, template_name, context = {'reset': reset}, recipient_list=[user.email])
```

Adicionar rota para nova view, recebendo como parâmetro a key para resetar a senha

```Python
urlpatterns = [
    # omitido código sem alteração
    url(r'^confirmar-nova-senha/(?P<key>\w+)$', views.password_reset_confirm, name='password_reset_confirm'),
]
```

Criar os novos templates:
* ```password_reset_mail.html```: Que contém o conteúdo do e-mail com o link para resetar a senha.
* ```password_reset_confirm.html```: Template de confirmação da senha criada ou exibe o form para criar a senha.

No template ```password_reset_mail.html``` a tag ```url``` do Django receberá um segundo parametro ```reset.key``` passado via contexto com o campo ```key``` do respectivo model. A tag ```url``` retorna a url relativa, para esta lição, será adicionado o domínio, mas em aulas posteriores será corrigido usando os recursos do Django.

```Django
<p>
    Para criar uma nova senha, acesse o link: <a href="http://127.0.0.1:8000{% url 'accounts:password_reset_confirm' reset.key %}">Criar nova senha</a>
</p>
```

O template ```password_reset_confirm.html``` tem a estrutura conhecida de forms anteriores.

```Django
{% extends 'base.html' %}

{% block content %}
<div class="pure-g-r content-ribbon">
    <div class="pure-u-1">
        {% if success %}
            <p>Senha criada com sucesso!</p>
        {% else %}
            <h2>Informe sua nova senha</h2>
            <form action="" class="pure-form pure-form-stacked" method="post">
                {% csrf_token %}
                <fieldset>
                    {{ form.non_field_errors }}
                    
                    {% for field in form %}
                        <div class="pure-control-group">
                            {{ field.label_tag }}
                            {{ field }}
                            {{ field.errors }}
                        </div>
                    {% endfor %}
                    
                    <div class="pure-controls">
                        <button type="submit" class="pure-button pure-button-primary">
                            Enviar
                        </button>
                    </div>
                </fieldset>
            </form>
        {% endif %}
    </div>
</div>

{% endblock content %}
```