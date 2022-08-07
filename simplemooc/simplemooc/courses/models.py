from django.db import models


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

    class Meta:
        verbose_name = "course"
        verbose_name_plural = "courses"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("course_detail", kwargs={"pk": self.pk})
