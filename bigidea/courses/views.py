from django.shortcuts               import render, get_object_or_404, redirect
from django.contrib                 import messages
from django.contrib.auth.decorators import login_required

from bigidea.courses.models         import Course, Enrollment, Announcement, Lesson, Material
from bigidea.courses.forms          import ContactCourse, CommentForm
from bigidea.courses.decorators     import enrollment_requered

# Create your views here.
def index(request):
	template_name = 'courses/index.html'
	courses = Course.objects.all()
	context = {"courses": courses}

	return render(request, template_name, context)

# def details(request, pk):
# 	template_name = 'courses/details.html'
# 	courses = get_object_or_404(Course, pk = pk)
# 	context = {"course": courses}

# 	return render(request, template_name, context)

def details(request, slug):
    template_name = 'courses/details.html'
    courses       = get_object_or_404(Course, slug = slug)
    form          = ContactCourse()
    context = {"course": courses, "form"  : form} 

    if request.method == 'POST':
        form = ContactCourse(request.POST)
        if form.is_valid():
            context['is_valid'] = True
            form.send_email(courses)
            # Para acessar um determinado campo do formulario
            # print(form.cleaned_data['name'])
            print(form.cleaned_data)
            form = ContactCourse()

    return render(request, template_name, context)

@login_required
def enrollment(request, slug):
    course     = get_object_or_404(Course, slug = slug)
    enrollment, created = Enrollment.objects.get_or_create(user = request.user,
                                                           course = course)
    
    if created:
        messages.success(request, "Você foi inscrito no curso com sucesso!")
        enrollment.active()
    else:
        messages.info(request, "Você já está inscrito no curso!")

    return redirect('dashboard')

@login_required
def undo_enrollment(request, slug):
    print("Request: ", request)
    template   = 'courses/undo_enrollment.html'
    course     = get_object_or_404(Course, slug = slug)
    enrollment = get_object_or_404(Enrollment, user = request.user, course = course)
    context = {} 
    
    if request.POST:
        enrollment.delete()
        messages.success(request, "Sua inscrição foi cancelada com sucesso!")
        return redirect('dashboard')
        
    context  = {"enrollment": enrollment, "course": course}

    return render(request, template, context)

@login_required
@enrollment_requered
def announcements(request, slug):
    template = 'courses/announcements.html'
    course   = request.course
    context  = {} 

    context  = {"course": course, "announcements": course.announcements.all()}

    return render(request, template, context)

@login_required
@enrollment_requered
def show_announcement(request, slug, pk):
    template = 'courses/show_announcement.html'
    course   = request.course
    form     = CommentForm(request.POST or None)
    context  = {} 

    announcement  = get_object_or_404(course.announcements.all(), pk = pk)

    if form.is_valid():
        comment = form.save(commit = False)
        comment.user = request.user
        comment.announcement = announcement
        comment.save()
        messages.success(request, "Sua comentário foi enviado com sucesso")

    context = {"course": course, "announcements": announcement, "form": form}

    return render(request, template, context)

@login_required
@enrollment_requered
def lessons(request, slug):
    template = 'courses/lessons.html'
    course   = request.course
    lessons  = course.release_lessons()

    if request.user.is_staff:
        lessons = course.lessons.all()

    context  = {"course": course, "lessons": lessons}

    return render(request, template, context)

@login_required
@enrollment_requered
def lesson(request, slug, pk):
    template = 'courses/lesson.html'
    course   = request.course
    lesson = get_object_or_404(Lesson, pk=pk, course=course)
    
    if not request.user.is_staff and not lesson.is_available():
        messages.error("Esta aula não está disponível")
        return redirect("lessons", slug=course.slug)

    context  = {"course": course, "lesson": lesson}

    return render(request, template, context)

@login_required
@enrollment_requered
def material(request, slug, pk):
    template = 'courses/material.html'
    course   = request.course
    material = get_object_or_404(Material, pk=pk, lesson__course=course)
    lesson   = material.lesson
    
    print("Curso: ", course)
    print("Aula: ", lesson)
    print("Material: ", material)
    print("material.is_embedded(): ", bool(material.is_embedded()))
    
    if not request.user.is_staff and not lesson.is_available():
        messages.error("Este material não está disponível")
        return redirect("lessons", slug=course.slug, pk=lesson.pk)
    
    if not material.is_embedded():
        return redirect(material.file.url)

    context  = {"course": course, "lesson": lesson, "material": material,}

    return render(request, template, context)