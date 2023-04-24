from django.contrib import admin
from django.urls import path
from AppUsuarios.views import chatear, editarPerfil, registro, mostrar_perfiles, login_request
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('registro/', registro, name='registro'),
    path('login', login_request, name='login'),
    path('perfiles/', mostrar_perfiles, name='perfiles'),
    path('editar_perfil/', editarPerfil, name='editar_perfil'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('chat/<id>', chatear, name='chat'),
]
