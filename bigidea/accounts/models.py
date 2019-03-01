import re

from django.conf                import settings
from django.db                  import models
from django.core                import validators
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin, UserManager)

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):

	username    = models.CharField("Nome do Usuário", max_length=30, unique = True,
				  validators=[validators.RegexValidator(re.compile('^[\w.@+-]+$'), 
				  "O nome de usuário só pode conter letras, digitos ou caracteres: @ . + - _",
				  'invalid')])
	email       = models.EmailField("Email", unique = True)
	name        = models.CharField("Nome", max_length=100, blank = True)
	is_active   = models.BooleanField("Está ativo?", blank = True, default = True)
	is_staff    = models.BooleanField("É da equipe?", blank = True, default = False)
	date_joined = models.DateTimeField("Data de Entrada", auto_now_add = True)

	objects = UserManager()

	USERNAME_FIELD  = 'username'
	REQUIRED_FIELDS = ['email']

	def __str__(self):
		return self.name or self.username

	def get_short_name(self):
		return self.username

	def get_full_name(self):
		return str(self)

	class Meta:
		verbose_name        = "Usuário"
		verbose_name_plural = "Usuários"
		ordering            = ['username']

class PasswordReset(models.Model):
	# related_name é importante para setar o nome do relacionamento entre os 
	# objetos User(Pai) e PasswordReset(Filho) no banco
	user       = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name = "Usuário", 
		                           on_delete=models.CASCADE, related_name = 'resets')
	key        = models.CharField("Chave", max_length = 100, unique = True)
	created_at = models.DateTimeField('Criado em', auto_now_add = True)
	# O blank indica que este atributo não é obrigatorio no caso da criação de um formulario
	confirmed  = models.BooleanField('Confirmado?', default = False, blank = True) 
    
	def __str__(self):
		return '{0} em {1}'.format(self.user, self.created_at)

	class Meta:
		verbose_name = 'Nova Senha'
		verbose_name_plural = 'Novas Senhas'
		# Ordenação de forma decrescente e por data
		ordering = ['-created_at']
        