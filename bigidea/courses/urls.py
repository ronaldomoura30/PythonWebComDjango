from django.urls import path

import bigidea.courses.views as views

urlpatterns = [ 
	#path("<int:pk>/", views.details, name="details"),
	path(""           , views.index, name="cursos"),
	path("<slug:slug>", views.details, name="details"),
	path("inscricao/<slug:slug>", views.enrollment, name="enrollment"),
	#path("anuncios/<slug:slug>", views.announcements, name="announcements"),
	path("<slug:slug>/anuncios", views.announcements, name="announcements"),
	path("<slug:slug>/anuncios/<pk>", views.show_announcement, name="show_announcement"),
	path("cancelar-inscricao/<slug:slug>", views.undo_enrollment, name="undo_enrollment"),
	path("<slug:slug>/aulas", views.lessons, name="lessons"),
	path("<slug:slug>/aulas/<pk>", views.lesson, name="lesson"),
	path("<slug:slug>/materiais/<pk>", views.material, name="material"),
]