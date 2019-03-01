from django                     import forms
from django.conf                import settings
from django.contrib.auth.forms  import UserCreationForm
from django.contrib.auth        import get_user_model
#from django.contrib.auth.models import User

from bigidea.core.utils         import generate_hash_key
from bigidea.core.mail          import send_email_template
from bigidea.accounts.models    import PasswordReset

User = get_user_model()

class PasswordResetForm(forms.Form):
    email = forms.EmailField(label = "E-mail")

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            return email
        raise forms.ValidationError("Nenhum usuário encontrado com este email")

    def save(self):
        user = User.objects.get(email=self.cleaned_data['email'])
        key = generate_hash_key(user.username)
        reset = PasswordReset(key=key, user=user)
        reset.save()
        template_name = 'accounts/password_reset_mail.html'
        subject = 'Criar nova senha no Big Idea'
        context = {
            'reset': reset,
        }
        send_email_template(subject, template_name, context, [settings.EMAIL_HOST_USER],
                            [user.email])

class RegisterForm(forms.ModelForm):

    password1 = forms.CharField(label = "Senha", widget = forms.PasswordInput)
    password2 = forms.CharField(label = "Confirmação de Senha", widget = forms.PasswordInput)


    # Verificando se as senhas são válidas e se são iguais
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("A senha de confirmação não está correta",
                                         code="password_mismatch")
        
        return password2

    # Metodo para salvar usuário cadastrado no banco
    def save(self, commit = True):
        user = super(RegisterForm, self).save(commit = False)
        user.set_password(self.cleaned_data['password1'])

        # user.email = self.cleaned_data['email']
        if commit:
            user.save()
    
        return user

    
    # def clean_email(self):
    #     email = self.cleaned_data['email']

    #     if User.objects.filter(email=email).exists():
    #         raise forms.ValidationError("Já existe usuário com este email")

    #     return email

    class Meta:
        model = User
        # Lista de campos que podem ser alterados
        fields = ['username', 'email']


class EditAccountForm(forms.ModelForm):
    
    def clean_email(self):
        email = self.cleaned_data['email']

        # OBS.: O exclude verifica se todos os outros usuário tem o email com exceção do usuário atual
        querySet = User.objects.filter(email=email).exclude(pk=self.instance.pk)

        if querySet.exists():
            raise forms.ValidationError("Já existe usuário com este email")

        return email

    class Meta:
        model  = User
        fields = ['username', 'email', 'name']
        #fields = ['username', 'email', 'first_name', 'last_name']
    	