from django.contrib import admin
from django.urls import path
from AppPaginas.views import *

urlpatterns = [
    path('verPagina/<id>', verPagina, name='verPagina'),
    path('agregarDestino', agregarDestino, name='agregarDestino'),
    path('mostrarPaginas', mostrarPaginas, name='mostrarPaginas'),
    path('eliminarPagina/<id>', eliminarPagina, name='eliminarPagina'),
    
    
]