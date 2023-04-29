from django.shortcuts import render
from AppUsuarios.views import obtenerAvatar


def inicio(request):

    return render(request, "inicio.html", {'avatar':obtenerAvatar(request), 'footer':obtenerFooter(request), 'banner':obtenerBanner(request)})


def acerca_de_mi(request):

    return render(request, "acerca_de_mi.html", {'avatar':obtenerAvatar(request), 'footer':obtenerFooter(request)})

def obtenerFooter(request):
    
    return "/media/varios/abajo.png"

def obtenerBanner(request):
    
    return "/media/varios/Descubramos.png"



