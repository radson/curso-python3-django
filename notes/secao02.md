# Seção 2: Baterias Inclusas - Algumas coisas que vem com o Django

## 12. App Courses

### Objetivos

* Conhecer o ORM do Django
* Criar uma nova aplicação no projeto

### Etapas

```Shell
mkdir simplemooc/courses
python manage.py startapp startapp courses simplemooc/courses
```

Adicionar o app no settings

```Python
INSTALLED_APPS = [
    'simplemooc.courses',
]
```

Em courses/model.py criar a classe Course

```Python
class Course(models.Model):

    name = models.CharField("Nome", max_length=100)
    slug = models.SlugField("Atalho")
    description = models.TextField("Descrição", blank=True)
    start_date = models.DateField(
        "Data de Início", auto_now=False, auto_now_add=False, null=True, blank=True)
    image = models.ImageField("Imagem", upload_to='courses/images',
                              height_field=None, width_field=None, max_length=None)
    created_at = models.DateTimeField(
        "Criado em", auto_now=False, auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True, auto_now_add=False)
```
No settings.py definir o diretório para upload de arquivos de media requeridos pelo campo ImageField

```Python
MEDIA_ROOT = os.path.join(BASE_DIR, 'simplemooc', 'media')
```

Dependência para tratar o campo do tipo ImageField

```Shell
pip install Pillow
```

O final gerar as migrations

```Shell
python manage.py makemigrations
python manage.py migrate
```
## 13. Métodos do Model

### Objetivos

* Criar o gerenciamento de usuários, inicialmente feito via dentro da própria app e depois utilizando o disponível no Django

### Etapas

No model Course, modificar no campo image os parametros verbose_name, null, blank.

```Python
image = models.ImageField(upload_to='courses/images', verbose_name="Imagem",
                            height_field=None, width_field=None, max_length=None,
                            null=True, blank=True)
```

Após modificar o model executar a migration

```Shell
python manage.py makemigrations
python manage.py migrate
```

Com as migrations aplicadas, pode-se acessar o shell do projeto para instânciar o model e incluir novos registros

```Shell
python manage.py shell
```

Um prompt iterativo carregando as settings do projeto será executado, neste prompt pode-se executar os comandos:

```Python
from simplemooc.courses.models import Course
course = Course()
course.name = "Python na Web com Django"
from datetime import date
course.start_date = date.today()
course.save()
course.id
course.pk
```

O método save() faz parte da classe Models. O ID do registro é setado automaticamente não sendo necessário informar, podendo ser acessado pela propriedade id ou pk.

Para alterar, por exemplo a propriedade name, ainda na mesma sessão, basta atribuir o novo valor e o método ```save()```, o Django irá entender que se trata de uma atualização e fará um UPDATE no banco de dados.

```Python
course.name = "Python com Django"
course.save()
```

Para a exclusão do registro, usa-se o ```delete()```

```Python
course.delete()
```