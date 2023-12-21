# Seção 6: Deploy e Testes

## 69. Introdução a Testes

### Objetivos

* Introdução a testes automatizados em Django

### Etapas

Para usar a classe *Client* do módulo django.test.client, adicionar o valor `testserver` nos `ALLOWED_HOSTS` do `settings.py`

```Python
ALLOWED_HOSTS = ['localhost', 'testserver']
```

No shell do Django, é possível realizar alguns testes

```Bash
python manage.py shell
```

```Python
from django.test.client import Client
from django.urls.base import reverse

c = Client()
response = c.get('/')
response.status_code

response = c.get(reverse('accounts:dashboard'))
response.status_code # Retorna um 302 pois o usuário não está mais logado.

c.login(username='admin', password='123456')

response = c.get(reverse('accounts:dashboard'))
response.status_code # Retorna um 200 com usuário logado.

c.logout()
```

## 70. Testando Views

### Objetivos

* Introdução a testes automatizados em Django

### Etapas

Dentro do app core, no arquivo `tests.py` são definidos os testes. A documentação sobre [Testing tools](https://docs.djangoproject.com/pt-br/1.11/topics/testing/tools/) explica a diversidade de recursos para implementar testes no Django.


No arquivo `testes.py` deve-se definir uma classe para cada domínio de testes e cada método da classe representa um caso de teste que será executado.

```Python
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

class HomeViewTest(TestCase):
    def test_home_status_code(self):
        client = Client()
        response = client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)

    def test_home_template_used(self):
        client = Client()
        response = client.get(reverse('core:home'))
        self.assertTemplateUsed(response, 'home.html')
        self.assertTemplateUsed(response, 'base.html')
```

Neste caso foram definidos 2 testes, um para testar se o response code foi 200 para um GET na home. Outro teste para verificar se os templates foram usados ao acessar a url da home. 

Para executar os testes, utiliza-se o comando:

```Bash
python manage.py test
```

## 71. Testando Forms e E-mail

### Objetivos

* Implementar os testes relativos a  uma submissão de formulário

### Etapas

Na app `courses` adicionar o conteúdo para o arquivo `test.py`.

```Python
from django.core import mail
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.conf import settings

from .models import Course


class ContactCourseTestCase(TestCase):
    def setUp(self):
        self.course = Course.objects.create(name="Django", slug="django")

    def tearDown(self):
        self.course.delete()

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_contact_form_error(self):
        data = {"name": "Fulano de Tal", "email": "", "message": ""}
        client = Client()
        path = reverse("courses:details", args=[self.course.slug])
        response = client.post(path, data)
        self.assertFormError(response, "form", "email", "Este campo é obrigatório.")
        self.assertFormError(response, "form", "message", "Este campo é obrigatório.")

    def test_contact_form_success(self):
        data = {"name": "Fulano de Tal", "email": "admin@admin.com", "message": "Oi"}
        client = Client()
        path = reverse("courses:details", args=[self.course.slug])
        response = client.post(path, data)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [settings.CONTACT_EMAIL])
```

O método `setUp` serve para inicializa cada test case, neste caso cria um objeto do tipo Course. Já o método `tearDown` serve para realizar atividades quando o teste case for concluído. Respectivamente o `setUpClass`  e o `tearDownClass` são executados antes e depois de todos os testes cases. 

O test case `test_contact_form_error` verifica se as mensagens de erro do form são exibidas quando os campos requeridos são vazios. O test case `test_contact_form_success` verifica a quantidade de e-mails enviada é igual a 1 e se o campo 'Para' do e-mail é o mesmo configurado no settings.


## 72. Testando Models com model-mommy

### Objetivos

* Usando o model-mommy para criar dados aleatórios para testes
* Criar uma estrutura de testes para quando são em grande quantidade

### Etapas

No app `courses`, adicionar um novo módulo `tests` que irá abrigar os arquivos de testes separados por componentes da aplicação, facilitando assim a organização.

```Bash
cd courses
mkdir tests
> tests/__init__.py
> tests/test_models.py
> tests/test_views.py
mv tests.py tests/test_forms.py 
```

O arquivo `tests.py` continha um teste de form, e vou movido para `tests/test_form.py`. 

Instalar o `model-mommy` para geração de dados aleatórios para os testes.

```Bash
pip install model_mommy
```

Para fazer uso do `model_mommy`, será criado um novo test case de models no arquivo `test_models.py`, com o conteúdo a seguir:

```Python
from django.test import TestCase
from simplemooc.courses.models import Course
from model_mommy import mommy

class CourseManagerTestCase(TestCase):
    def setUp(self):
        self.courses_django = mommy.make(
            "courses.Course", name="Python na Web com Django", _quantity=10
        )

        self.courses_dev = mommy.make(
            "courses.Course", name="Python para Devs", _quantity=10
        )

    def tearDown(self):
        Course.objects.all().delete()

    def test_course_search(self):
        search = Course.objects.search("django")
        self.assertEqual(len(search), 10)
        search = Course.objects.search("devs")
        self.assertEqual(len(search), 10)
        search = Course.objects.search("python")
        self.assertEqual(len(search), 20)
```

No `setUp`, usando o mommy informa-se o nome do model, os campos que serão utilizados para criação e a quantidade de registros a serem criados. No `tearDown`, todos os objetos criados são excluídos.

O `test_course_search` faz o teste para conferir se a quantidade de registros a partir da string procurada retornar a quantidade de registros conforme esperado.

Para executar os testes, no arquivo `__init__.py`, deve-se realizar as chamadas conforme a seguir:

```Python
from .test_forms import ContactCourseTestCase
from .test_models import CourseManagerTestCase
```

Para executar os testes, continua o comando:

```Bash
python manage.py test
```

## 73. Introdução ao Deploy no Heroku
## 74. Ajustando o Deploy no Heroku

### Objetivos

* Preparar a aplicação para executar em um servidor em produção com a plataforma Heroku

### Etapas

A plataforma Heroku deixou de ser gratuita em 2023, por isso a aula de deploy no Heroku não será possível reproduzir na mesma plataforma. 

https://coodesh.com/blog/candidates/heroku-acabou-e-agora-veja-alternativas/
