from django.urls import path
import bigidea.core.views as views

urlpatterns = [ 
	path(""        , views.home, name="home"),
	path("contato/", views.contact, name="contact"),
]