# Seção 5: Acessando o Curso

## 52. Modelagem da Inscrição

### Objetivos

* Iniciar o desenvolvimento das aplicações do domínio do curso (ex. aulas, inscrições, etc). Nesta aula será criado o model de inscrições

### Etapas

No `models.py` da app `Courses` adicionar um novo model para tratar das inscrições chamado `Enrollment`.

```Python
from django.conf import settings

# omitido código sem alteração

class Enrollment(models.Model):

    STATUS_CHOICE = (
        (0, 'Pendente'),
        (1, 'Aprovado'),
        (2, 'Cancelado'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             verbose_name='Usuário', related_name='enrollments')

    course = models.ForeignKey(Course, verbose_name='enrollments')

    status = models.IntegerField(
        'Situação', choices=STATUS_CHOICE, default=0, blank=True)
    created_at = models.DateTimeField(
        'Criado em', auto_now=False, auto_now_add=True)
    update_at = models.DateTimeField(
        'Atualizado em', auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name = 'Inscrição'
        verbose_name_plural = 'Inscrições'
        unique_together = (('user', 'course'),)
```

Em seguida realizar a migração no banco de dados.

```Shell
python manage.py makemigrations
python manage.py migrate
```

## 53. Implementando a inscrição no Curso

### Objetivos

* Prapara o sistema para permitir a inscrição do usuário em um curso.

### Etapas

Na app `courses` adicionar em `views.py` nova view para permitir inscrição no curso. Esta view usa a `slug` do curso para selecionar o curso no banco de dados

```Python
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from .models import Enrollment

# omitido código sem alteração

@login_required
def enrollment(request, slug):
    course = get_object_or_404(Course, slug=slug)
    enrollment, created = Enrollment.objects.get_or_create(
        user=request.user, course=course)

    return redirect('accounts:dashboard')
```

No model `Enrollment`, alterar o valor default do campo `status` 1 (aprovado). Posteriormente uma lógica pode ser adicionada para tratar melhor.

```Python
# omitido código sem alteração
status = models.IntegerField(
        'Situação', choices=STATUS_CHOICE, default=1, blank=True)
```

No arquivo de rotas `urls.py` adicionar nova rota para inscrição

```Python
urlpatterns = [
    # omitido código sem alteração
    url(r'^(?P<slug>[\w_-]+)/inscricao/$', views.enrollment, name='enrollment'),
]
```

No template `details.html`, na tag que contem a label *Inscreva-se*, adicionar a url passando a slug como parâmetro.

```Django
<a href={% url 'courses:enrollment' course.slug %} class="pure-button primary-button">Inscreva-se</a>
```