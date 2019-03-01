# -*- coding: utf-8 -*-
from django.conf       import settings
from django.utils      import timezone
from django.db         import models
from django.dispatch   import receiver
from django.urls       import reverse

from bigidea.core.mail import send_email_template

class CourseManager(models.Manager):

	def search(self, query):
		return self.get_queryset().filter( \
			models.Q(name__icontains = query) | models.Q(description__icontains = query))

class Course(models.Model):
	#Blank = True (Não é obrigatório)
	#null = Objeto None(null) no banco

	name        = models.CharField("Nome", max_length = 100)
	slug        = models.SlugField("Atalho", unique= True, max_length = 60)
	description = models.TextField("Descrição Curta", blank = True)
	about       = models.TextField("Descrição Longa do Curso", blank = True)
	start_date  = models.DateField("Data de Início", null = True, blank = True)
	image       = models.ImageField(upload_to="courses/imagens", verbose_name = "Image",
									null = True, blank = True)
	create_at   = models.DateTimeField("Criado em", auto_now_add = True)
	update_at   = models.DateTimeField("Atualizado em", auto_now = True)

	objects = CourseManager()

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('details', args=[self.slug])

	def release_lessons(self):
		today = timezone.now().date()
		return self.lessons.filter(release_date__gte=today)

class Lesson(models.Model):
	course       = models.ForeignKey(Course, verbose_name = "Curso", related_name = "lessons",
							         on_delete = models.CASCADE)

	name         = models.CharField(verbose_name="Nome", max_length=100)
	description  = models.TextField(verbose_name="Descrição", blank=True)
	release_date = models.DateField(verbose_name="Data de Liberação", blank=True, null=True) 
	number       = models.IntegerField(verbose_name="Sequência de aulas", blank=True, default=0)
	created_at   = models.DateTimeField(verbose_name="Criado em", auto_now_add = True)
	updated_at   = models.DateTimeField(verbose_name="Atualizado em", auto_now = True) 

	def __str__(self):
		return self.name
	
	def is_available(self):
		if self.release_date:
			today = timezone.now().date()
			return self.release_date >= today

	class Meta:
		verbose_name        = "Aula"
		verbose_name_plural = "Aulas"
		ordering            = ['number']

class Material(models.Model):

	lesson     = models.ForeignKey(Lesson, verbose_name = "Aula", related_name = "materials",
				        		   on_delete = models.CASCADE)

	name       = models.CharField(verbose_name="Nome", max_length=100)
	embedded   = models.TextField(verbose_name="Arquivo", blank=True)
	file       = models.FileField(upload_to="lessons/materials", blank=True, null=True)
	created_at = models.DateTimeField(verbose_name="Criado em", auto_now_add = True)
	updated_at = models.DateTimeField(verbose_name="Atualizado em", auto_now = True)
    
	def __str__(self):
		return self.name

	def is_embedded(self):
		return bool(self.embedded)

	class Meta:
		verbose_name        = "Matérial"
		verbose_name_plural = "Materiais"

# Classe Meta é uma classe contida em toda classe criada no Django
class Meta:

	verbose_name        = "Curso"
	verbose_name_plural = "Cursos"
	ordering            = ['name']

# Classe responsavel pela inscrição do usúário no curso 
class Enrollment(models.Model):

	STATUS_CHOICES = ( (0, 'Pendente'), (1, "Aprovado"), (2, "Cancelado"))

	user   = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name = "Usuário", 
		                       on_delete=models.CASCADE, related_name = 'enrollments')

	course = models.ForeignKey(Course, verbose_name = "Curso", related_name = 'enrollments',
							   on_delete = models.CASCADE)

	status = models.IntegerField(verbose_name = "Situação", default = 0,
								 choices = STATUS_CHOICES, blank = True)

	create_at   = models.DateTimeField("Criado em", auto_now_add = True)
	update_at   = models.DateTimeField("Atualizado em", auto_now = True) 
	
	def active(self):
		self.status = 1
		self.save()

	def is_approved(self):
		return self.status == 1
		
	class Meta:

		verbose_name        = "Inscrição"
		verbose_name_plural = "Incrições"
		unique_together     =  (('user', 'course'))
		ordering            = ['course']

class Announcement(models.Model):

	course = models.ForeignKey(Course, verbose_name = "Curso", related_name = "announcements",
							   on_delete = models.CASCADE)

	title   = models.CharField(verbose_name = "Título", max_length=100)
	content = models.TextField(verbose_name = "Conteúdo")

	created_at   = models.DateTimeField("Criado em", auto_now_add = True)
	updated_at   = models.DateTimeField("Atualizado em", auto_now = True) 
	
	def __str__(self):
		return self.title

	class Meta:

		verbose_name        = "Anúncio"
		verbose_name_plural = "Anúncios"
		ordering            = ['-created_at']

class Comment(models.Model):

	announcement = models.ForeignKey(Announcement, verbose_name = "Comentário",
									 related_name = 'comments', on_delete = models.CASCADE)

	user         = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name = "Usuário", 
		                             on_delete=models.CASCADE, related_name = 'comments')

	comment      = models.TextField(verbose_name = "Comentário")
	created_at   = models.DateTimeField("Criado em", auto_now_add = True)
	updated_at   = models.DateTimeField("Atualizado em", auto_now = True) 
	
	class Meta:

		verbose_name        = "Comentário"
		verbose_name_plural = "Comentários"
		ordering            = ['-created_at']

@receiver(models.signals.post_save, sender=Announcement)
def post_save_announcement(instance, created, **kwargs):
	if created:
		template_name = "courses/announcement_mail.html"
		subject = instance.title
		context = {'announcement': instance}

		enrollments = Enrollment.objects.filter(course=instance.course, status=1)

		for enrollment in enrollments:
			recipient_list = [enrollment.user.email]

			print("Email: ", recipient_list)

			send_email_template(subject, template_name, context, recipient_list, [settings.EMAIL_HOST_USER])