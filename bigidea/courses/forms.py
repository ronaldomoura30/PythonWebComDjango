from django           import forms
from django.conf      import settings

from bigidea.core.mail      import send_email_template
from bigidea.courses.models import Comment

class ContactCourse(forms.Form):

    name    = forms.CharField(label = "Nome", max_length = 100, required  = True)
    email   = forms.EmailField(label = "Email", required  = True)
    message = forms.CharField(label = "Mesagem / Dúvida", widget = forms.Textarea,
    						  required  = True)

    def send_email(self, course):
    	template_name = 'courses/contact_email.html'

    	subject = 'Dúvidas sobre o Curso %s' %course

    	context = {'name'   : self.cleaned_data['name'],
    			   'email'  : self.cleaned_data['email'],
    	           'message': self.cleaned_data['message']}

    	send_email_template(subject, template_name, context, 
    		                [settings.EMAIL_HOST_USER], self.cleaned_data['email'])

class CommentForm(forms.ModelForm):

    class Meta:
        model  = Comment
        fields = ['comment']