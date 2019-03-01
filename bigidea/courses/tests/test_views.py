from django.core        import mail
from django.test        import TestCase
from django.test.client import Client
from django.urls        import reverse
from django.conf        import settings

from bigidea.courses.models import Course

# Create your tests here.
class HomeViewTest(TestCase):

	def setUp(self):
		self.course = Course

	def test_home_status_code(self):
		client   = Client()
		response = client.get(reverse("home"))
		self.assertEqual(response.status_code, 200)

	def test_home_template_used(self):
		client   = Client()
		response = client.get(reverse("home"))
		self.assertTemplateUsed(response, "home.html")
		self.assertTemplateUsed(response, "base.html")

class ContactCourseTestCase(TestCase):

	# Metodo que será executado antes de cada metodo de teste criado (Metodos Auxiliares)
	def setUp(self):
		self.course = Course.objects.create(name="Django", slug="django")		

	# Metodo que será executado apos cada metodo de teste criado (Metodos Auxiliares)
	def tearDown(self):
		self.course.delete()

	def teste_contact_form_success(self):
		data     = {'name': 'Fulano de Tal', "email": "fulano@gmail.com", "message": "Oi"}
		client   = Client()
		path     = reverse('details', args=[self.course.slug])
		response = client.post(path, data)
		# Testou se foi enviado um email
		self.assertEqual(len(mail.outbox), 1)

		# Testou se o usuário de envido do email foi o settings.EMAIL_HOST_USER
		self.assertEqual(mail.outbox[0].to, [settings.EMAIL_HOST_USER])
		