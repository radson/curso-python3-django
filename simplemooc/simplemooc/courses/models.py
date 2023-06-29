from django.conf import settings
from django.db import models

from simplemooc.core.mail import send_mail_template


class CourseManager(models.Manager):

    def search(self, query):
        return self.get_queryset().filter(models.Q(name__icontains=query) |
                                          models.Q(description__icontains=query))


class Course(models.Model):

    name = models.CharField("Nome", max_length=100)
    slug = models.SlugField("Atalho")
    description = models.TextField("Descrição simples", blank=True)
    about = models.TextField("Sobre o curso", blank=True)
    start_date = models.DateField(
        "Data de Início", auto_now=False, auto_now_add=False, null=True, blank=True)
    image = models.ImageField(upload_to='courses/images', verbose_name="Imagem",
                              height_field=None, width_field=None, max_length=None,
                              null=True, blank=True)
    created_at = models.DateTimeField(
        "Criado em", auto_now=False, auto_now_add=True)
    update_at = models.DateTimeField(
        'Atualizado em', auto_now=True, auto_now_add=False)

    @models.permalink
    def get_absolute_url(self):
        return ("courses:details", (), {"slug": self.slug})

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"
        ordering = ['name']

    def __str__(self):
        return self.name

    objects = CourseManager()


class Lesson(models.Model):
    name = models.CharField("Nome", max_length=100)
    description = models.TextField('Descrição', blank=True)
    number = models.IntegerField('Número (ordem)', blank=True, default=0)
    release_date = models.DateField('Data de Liberação', blank=True, null=True)

    course = models.ForeignKey(
        Course, verbose_name='Curso', related_name='lessons')

    created_at = models.DateTimeField(
        'Criado em', auto_now=False, auto_now_add=True)
    update_at = models.DateTimeField(
        'Atualizado em', auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Aula'
        verbose_name_plural = 'Aulas'
        ordering = ['number']


class Material(models.Model):
    name = models.CharField("Nome", max_length=100)
    embedded = models.TextField('Vídeo embedded', blank=True)
    file = models.ImageField(
        upload_to='lessons/materials', null=True, blank=True)

    lesson = models.ForeignKey(
        Lesson, verbose_name='aula', related_name='materials')

    def is_embedded(self):
        return bool(self.embedded)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Material'
        verbose_name_plural = 'Materiais'


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
        'Situação', choices=STATUS_CHOICE, default=1, blank=True)
    created_at = models.DateTimeField(
        'Criado em', auto_now=False, auto_now_add=True)
    update_at = models.DateTimeField(
        'Atualizado em', auto_now=True, auto_now_add=False)

    def is_approved(self):
        return self.status == 1

    class Meta:
        verbose_name = 'Inscrição'
        verbose_name_plural = 'Inscrições'
        unique_together = (('user', 'course'),)


class Announcement(models.Model):
    course = models.ForeignKey(
        Course, verbose_name='Curso', related_name='announcements')
    title = models.CharField('Título', max_length=100)
    content = models.TextField('Conteúdo')
    created_at = models.DateTimeField(
        'Criado em', auto_now=False, auto_now_add=True)
    update_at = models.DateTimeField(
        'Atualizado em', auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Anúncio'
        verbose_name_plural = 'Anúncios'
        ordering = ['-created_at']


class Comment(models.Model):
    announcement = models.ForeignKey(
        Announcement, verbose_name='Anúncio', related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='usuário')
    comment = models.TextField('Comentário')
    created_at = models.DateTimeField(
        'Criado em', auto_now=False, auto_now_add=True)
    update_at = models.DateTimeField(
        'Atualizado em', auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'
        ordering = ['created_at']


def post_save_announcement(instance, created, **kwargs):
    if created:
        subject = instance.title
        context = {
            'announcement': instance
        }

        template_name = 'courses/announcement_mail.html'
        enrollments = Enrollment.objects.filter(
            course=instance.course, status=1)

        for enrollment in enrollments:
            recipient_list = [enrollment.user.email]
            send_mail_template(subject, template_name, context, recipient_list)


models.signals.post_save.connect(
    post_save_announcement, sender=Announcement,
    dispatch_uid='post_save_announcement')
