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