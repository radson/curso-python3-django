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