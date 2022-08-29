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

## 14. Model objects

### Objetivos

* Utilizar o recurso de Querysets

### Etapas

Continuando o exemplo da aula anterior, acessar o shell do Django e inserir ao menos 2 registros

```Python
django = Course(name="Python com Django", slug="django")
django.save()
django.pk
python_dev = Course(name="Python para Devs", slug="python-dev")
python_dev.save()
python_dev.pk
```

Agora será feito o uso dos objects da classe Model, que é um gerenciador conforme consta na documentação:

>Um “manager” é a interface através da qual as consultas de banco de dados são fornecidas para os modelos do Django. Pelo menos um Manager existe para cada modelo em uma aplicação Django.
[Django Doc - Managers](https://docs.djangoproject.com/pt-br/1.11/topics/db/managers/)

O método ```all()``` retorna a referência a todos os objetos do model. O Django utiliza o conceito de lazy load, então os registros só serão consultados no banco de dados quando são realmente acessados.

```Python
courses = Course.objects.all()
for course in courses:
    print(course.name)
```

Outro recurso é o ```filter()``` que permite filtrar os objetos de acordo com as propriedades inseridas como parametros do método. No exemplo a seguir irá retornar um Queryset com apenas um registo que corresponde ao filtro.

```Python
courses = Course.objects.filter(slug='django')
print(courses)
```
O Django permite que o  ```filter()``` seja aninhado com outro ```filter()``` e que mais de um parametro da busca sejam informados separados por vírgula. 
Outro recurso é o [filtro de campos](https://docs.djangoproject.com/pt-br/1.11/topics/db/queries/#field-lookups) que permite realizar o mesmo que a cláusula WHERE do SQL. No exemplo a segui será usado o ```icontais``` para busca textual no campo ```name``` ignorando o tipo de caixa.

```Python
courses = Course.objects.filter(name__icontains='python')
print(courses)
```

Cada QuerySet tem um método ```delete()```, o qual [deleta](https://docs.djangoproject.com/pt-br/1.11/topics/db/queries/#deleting-objects) todos os membros daquele QuerySet.

```Python
courses.delete()
Course.objects.all()
```


## 15. Custom Manager

### Objetivos

* Aprofundar o conhecimento sobre os managers e querysets

### Etapas

Criar uma nova classe no models.py para implementar um método de busca utilizando ```get_queryset``` e o recurso de field_lookup nos campos name ou description. Para implementar o OU do SQL utiliza-se a [classe Q](https://docs.djangoproject.com/pt-br/3.2/ref/models/querysets/#q-objects)

```Python
class CourseManager(models.Manager):

    def search(self, query):
        return self.get_queryset().filter(models.Q(name__icontains=query) |
                                          models.Q(description__icontains=query))
```

Na classe Courses, alterar para usar o Manager customizado em vez do padrão do Django:

```Python
class Course(models.Model):

    objects = CourseManager()
```

Para testar, utilizando o shell e considerando os registros inseridos nas aulas anteriores. Esta consulta deverá retornar ao menos 2 objetos (aula anterior)

```Python
Course.objects.search('python')
```