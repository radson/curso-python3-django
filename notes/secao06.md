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