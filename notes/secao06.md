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