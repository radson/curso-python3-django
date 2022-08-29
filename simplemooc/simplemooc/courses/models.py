from django.db import models


class CourseManager(models.Manager):

    def search(self, query):
        return self.get_queryset().filter(models.Q(name__icontains=query) |
                                          models.Q(description__icontains=query))


class Course(models.Model):

    name = models.CharField("Nome", max_length=100)
    slug = models.SlugField("Atalho")
    description = models.TextField("Descrição", blank=True)
    start_date = models.DateField(
        "Data de Início", auto_now=False, auto_now_add=False, null=True, blank=True)
    image = models.ImageField(upload_to='courses/images', verbose_name="Imagem",
                              height_field=None, width_field=None, max_length=None,
                              null=True, blank=True)
    created_at = models.DateTimeField(
        "Criado em", auto_now=False, auto_now_add=True)
    update_at = models.DateTimeField(
        'Atualizado em', auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name = "course"
        verbose_name_plural = "courses"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("course_detail", kwargs={"pk": self.pk})

    objects = CourseManager()
