from django.shortcuts import render
from AppUsuarios.views import obtenerAvatar


def inicio(request):

    return render(request, "inicio.html", {'avatar':obtenerAvatar(request)})

