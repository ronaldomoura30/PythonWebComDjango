from django.urls               import path, include
from django.contrib.auth.views import LoginView, LogoutView

import bigidea.accounts.views as views

urlpatterns = [ 
    path("dashboard"      , views.dashboard, name='dashboard'),

    path("cadastre-se"    , views.register, name='register'),   
    path("editar"         , views.edit, name='edit'),
    path("editar-senha"   , views.edit_password, name='edit_password'),
    path("sair"           , LogoutView.as_view(next_page='home'), name='logout'),
    path("reset-senha"    , views.password_reset, name='password_reset'),
    path("entrar"         , LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path("confirmar-senha/<key>", views.password_reset_confirm, name='password_reset_confirm'),
]
