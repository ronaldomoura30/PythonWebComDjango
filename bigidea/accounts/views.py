from django.conf                    import settings 
from django.contrib                 import messages
from django.contrib.auth            import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms      import UserCreationForm, PasswordChangeForm, SetPasswordForm
from django.shortcuts               import render, redirect, get_object_or_404

from bigidea.core.utils             import generate_hash_key
from bigidea.accounts.forms         import RegisterForm, EditAccountForm, PasswordResetForm
from bigidea.accounts.models        import PasswordReset
from bigidea.courses.models         import Enrollment

# Create your views here.
@login_required()
def dashboard(request):
	template_name = 'accounts/dashboard.html'
	context = {}
	
	# context['enrollments'] = Enrollment.objects.filter(user = request.user)
	return render(request, template_name, context)

@login_required()
def edit(request):	
	template_name = 'accounts/edit.html'
	context       = {}

	if request.method == 'POST':
		form = EditAccountForm(request.POST, instance=request.user)
		if form.is_valid():
			form.save()
			messages.add_message(request, messages.SUCCESS, 
				                 'Os dados da sua conta foram alterados com sucesso')
			# messages.success(request, 'Os dados da sua conta foram alterados com sucesso')
			return redirect("dashboard")
			# form = EditAccountForm(instance = request.user)
			# context['success'] = True
	else:
		form = EditAccountForm(instance = request.user)

	context['form'] = form
	return render(request, template_name, context)


@login_required
def edit_password(request):
    template_name = 'accounts/edit_password.html'
    context       = {}

    if request.method == 'POST':
    	form = PasswordChangeForm(data=request.POST, user=request.user)

    	if form.is_valid():
        	form.save()
        	context['success'] = True
    else:
    	form = PasswordChangeForm(user=request.user)

    context['form'] = form
    return render(request, template_name, context)


def register(request):
	template_name = 'accounts/register.html'
	form          = RegisterForm()	

	if request.method == 'POST':
		form = RegisterForm(request.POST)

		if form.is_valid():
			user = form.save()
			user = authenticate(username = user.username, 
				                password = form.cleaned_data['password1'])

			login(request, user)
			return redirect(settings.LOGIN_REDIRECT_URL)

	context = {"form": form} 

	return render(request, template_name, context)

def password_reset(request):
	template_name = 'accounts/password_reset.html'
	context = {}
	# Se o POST estiver vazio então prenche com none.
 	# O mesmo que chamar PasswordResetForm() assim ele não é automaticamente validado
	form = PasswordResetForm(request.POST or None)
	
	if form.is_valid():
		# user  = User.objects.get(email = form.cleaned_data['email'])
		# key   = generate_hash_key(user.username)
		# reset = PasswordReset(key = key, user = user)
		form.save()
		messages.success(request, 'Email de reset de senha foi enviado para seu email')
		return redirect("login")
	else:
		messages.error(request, 'Email informado não é válido')

	context['form'] = form
	return render(request, template_name, context)

def password_reset_confirm(request, key):
	template_name = 'accounts/password_reset_confirm.html'

	context = {}

	reset = get_object_or_404(PasswordReset, key = key)

	form = SetPasswordForm(user = reset.user, data = request.POST or None)
	if form.is_valid():
		form.save()
		context['sucess'] = True  

	context['form'] = form
	return render(request, template_name, context)