from django.contrib import admin
from django.urls import path
from AppUsuarios.views import agregarAvatar, chatear, editar_usuario, registro, mostrar_perfiles, login_request, agregarPerfil, verPerfil, verMiPerfil, editar_mi_perfil
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('registro/', registro, name='registro'),
    path('login', login_request, name='login'),
    path('perfiles/', mostrar_perfiles, name='perfiles'),
    path('editar_usuario/', editar_usuario, name='editar_usuario'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('chat/<id>', chatear, name='chat'),
    path('agregarAvatar', agregarAvatar, name='agregarAvatar'),
    path('agregar_perfil', agregarPerfil, name='agregar_perfil'),
    path('ver_perfil_individual/<id>', verPerfil, name='verPerfil'),
    path('verMiPerfil', verMiPerfil, name='verMiPerfil'),
    path('editar_mi_perfil', editar_mi_perfil, name='editar_mi_perfil'),
    
]
