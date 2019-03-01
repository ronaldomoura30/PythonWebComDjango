from django.core        import mail
from django.test        import TestCase
from django.test.client import Client
from django.urls        import reverse
from django.conf        import settings

from bigidea.courses.models import Course
from bigidea.courses.forms  import ContactCourse

# Create your tests here.
class CoursesFormsTest(TestCase):

	# Metodo que será executado antes de cada metodo de teste criado (Metodos Auxiliares)
	def setUp(self):
		self.course = Course.objects.create(name="Django", slug="django")
		self.client = Client()	
		self.path   = reverse('details', args=[self.course.slug])

	# Metodo que será executado apos cada metodo de teste criado (Metodos Auxiliares)
	def tearDown(self):
		self.course.delete()

	# Testando se o form de contato do curso é válido
	def test_contact_form_valid(self):
		data = {'name': 'Fulano', 'email': 'fulano@gmail.com', 'message': 'Ementa do curso'}
		form = ContactCourse(data=data)
		self.assertTrue(form.is_valid())

	# Testando se o form de contato do curso é inválido
	def test_contact_form_invalid(self):
		data = {'name': '', 'email': 'fulano@gmail.com', 'message': 'Ementa do curso'}
		form = ContactCourse(data=data)
		self.assertFalse(form.is_valid())