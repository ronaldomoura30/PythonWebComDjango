from django.core        import mail
from django.test        import TestCase
from django.test.client import Client
from django.urls        import reverse
from django.conf        import settings

from model_mommy import mommy

from bigidea.courses.models import Course

class CourseManagerTestCase(TestCase):
	
	# Metodo que será executado antes de cada metodo de teste criado (Metodos Auxiliares)
	def setUp(self):
		self.courses = mommy.make("courses.Course", name='Python na Web com Django',
		                           _quantity=1)
		self.courses = mommy.make("courses.Course", name='Python para Devs',
		                           _quantity=1)
		self.client = Client()

	# Metodo que será executado apos cada metodo de teste criado (Metodos Auxiliares)
	def tearDown(self):
		for course in self.courses:
			course.delete()

	def test_course_search(self):
		search = Course.objects.search('django')
		self.assertEqual(len(search), 1)

		search = Course.objects.search('devs')
		self.assertEqual(len(search), 1)

		search = Course.objects.search('python')
		self.assertEqual(len(search), 2)
