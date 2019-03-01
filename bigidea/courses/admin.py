from django.contrib import admin

from .models import Course, Enrollment, Announcement, Comment, Lesson, Material

#Definindo uma classe para customizar o model no admin

# class MaterialInlineAdmin(admin.TabularInline):
	
# 	model = Material

class MaterialInlineAdmin(admin.StackedInline):
	
	model = Material

class CourseAdmin(admin.ModelAdmin):
	# Exibir colunas para a tabela Courses no admin
	list_display  = ['name', "slug", "start_date", "create_at"]

	#Set campos de pesquisa 
	search_fields = ['name', 'slug']

	#Preencher o campo slug com os valores do campo nome
	prepopulated_fields = {'slug': ('name', )}

class LessonAdmin(admin.ModelAdmin):
	# Exibir colunas para a tabela Aulas no admin
	list_display  = ['name', "number", "course", "release_date"]

	#Set campos de pesquisa 
	search_fields = ['name', 'course', 'description']

	#Filtro lateral
	list_filter   = ["created_at"] 

	inlines = [MaterialInlineAdmin]

# Register your models here.
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register([Enrollment, Announcement, Comment, Material])
