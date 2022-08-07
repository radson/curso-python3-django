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