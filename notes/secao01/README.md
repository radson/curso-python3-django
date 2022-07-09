## Aula 03 - Ambiente virtual

Criar ambiente virtual

$ virtualenv venv -p python3

Para ativar o ambiente:

$ source venv/bin/activate

Atualizando pacotes

```
pip install -U pip wheel setuptools
```

Pacotes extra para melhor gestão da qualidade do código
```sh
$ pip install flake8 mypy autopep8
```

Para desativar

```
$ deactivate
```


## Aula 04 - Configurando o Django

```
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

```sh
$ python manage.py migrate
$ python manage.py createsuperuser
```
Agora criar a primeira aplicação dentro do projeto

```sh
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