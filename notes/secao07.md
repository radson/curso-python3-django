# Seção 7: Fórum de Dúvidas

## 75. Modelagem do Fórum

### Objetivos

* Criar um app de Forum de Dúvidas sobre os cursos
* Utilizar bibliotecas criadas por terceiros para reaproveitar o código. Será integrada lib django-taggit

### Etapas

Com o venv habilitado, baixar a versão da lib django-taggit compatível com Django 1.11 utilizado neste projeto.

```Bash
pip install django-taggit==1.4.0
```

Integrar a lib ao projeto Django, adicionando a app `taggit` em `INSTALLED_APPS` no arquivo `settings.py`.

```Python
INSTALLED_APPS = [
    # outras apps instaladas foram omitidas
    'taggit',
]
```

Finaliar a instalação rodando as migrations necessárias ao taggit.

```Shell
python manage.py migrate
```

Agora criar nova app com nome 'Forum' dentro da estrutura do projeto `simplemooc`.

```Bash
mkdir simplemooc/forum
python manage.py startapp forum simplemooc/forum
```

Criar a modelagem da app Forum no arquivo `models.py` com dois objetos principais: Thread e Reply. 
O uso da lib taggit é através do campo `tags` que recebe um `TaggableManager`.

```Python
from django.conf import settings
from django.db import models
from taggit.managers import TaggableManager


class Thread(models.Model):

    title = models.CharField('Título', max_length=100)
    body = models.TextField('Mensagem')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Autor',
        related_name='threads'
        )
    views = models.IntegerField('Visualizações', blank=True, default=0)
    answers = models.IntegerField('Respostas', blank=True, default=0)
    tags = TaggableManager()
    
    created = models.DateField('Criado em', auto_now_add=True)
    modified = models.DateField('Modificado em', auto_now=True)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Tópico'
        verbose_name_plural = 'Tópicos'
        ordering = ['-modified']

class Reply(models.Model):

    reply = models.TextField('Resposta')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Autor',
        related_name='replys'
        )
    correct = models.BooleanField('Correta?', blank=True, default=False)

    created = models.DateField('Criado em', auto_now_add=True)
    modified = models.DateField('Modificado em', auto_now=True)        

    def __str__(self):
        return self.reply[:100]

    class Meta:
        verbose_name = 'Resposta'
        verbose_name_plural = 'Respostas'
        ordering = ['-correct', 'created']
```

## 76. Class-based views no Fórum Parte 1

### Objetivos

* Iniciar a implementação das views
* Conhecer a class-based views

### Etapas

Para implementar uma view a partir de um model, pode-se utilizar o recurso  `Base views` do Django. Mais detalhes na documentação sobre [Base Views](https://docs.djangoproject.com/en/1.11/ref/class-based-views/base/#base-views).

Iniciar a implementação no arquivo `views.py`, utilizando a classe [TemplateView](https://docs.djangoproject.com/en/1.11/ref/class-based-views/base/#templateview).

```Python
from django.shortcuts import render
from django.views.generic import TemplateView


class ForumView(TemplateView):
    template_name = 'forum/index.html'
```

Criar o diretório para templates

```Bash
mkdir -p forum/templates/forum
> forum/templates/forum/index.html
```

Criar o `urls.py` na app Forum informando a view index

```Python
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
```

Instalar a app Forum em settings e realizar a migração que faltou na aula anterior.

```Python
INSTALLED_APPS = [
    # outras apps instaladas foram omitidas
    'simplemooc.forum',
]
```

Criar e executar as migrates.

```Shell
python manage.py makemigrations
python manage.py migrate
```