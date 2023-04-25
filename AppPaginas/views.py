from django.shortcuts import render
from AppPaginas.forms import PaginaForm
from AppUsuarios.views import obtenerAvatar, obtenerFooter
from AppPaginas.models import *

def agregarDestino(request):
    if request.method == "POST":

        form = PaginaForm(request.POST, request.FILES)
        
        if form.is_valid():

            u = User.objects.get(username=request.user)

            pagina = Pagina (autor=u, imagen=form.cleaned_data['imagen'], titulo = form.cleaned_data['titulo'], subtitulo = form.cleaned_data['subtitulo'], cuerpo = form.cleaned_data['cuerpo'])
            
            pagina.save()
            
            return render(request, 'pagina_individual.html', {"mensaje": "Pagina creada correctamente", 'avatar':obtenerAvatar(request), 'footer':obtenerFooter(request)})
        
    else: 

        form = PaginaForm()

    return render (request, "crear_pagina.html", {"form": form, 'avatar':obtenerAvatar(request)})

def mostrarPaginas(request):
    paginas = Pagina.objects.all()

    if paginas:
        return render(request, "mostrar_paginas.html", {"paginas":paginas, 'avatar':obtenerAvatar(request), 'footer':obtenerFooter(request)})
    else:
        mensaje="No hay paginas para mostrar aun"
        return render(request, "mostrar_paginas.html", {'mensaje':mensaje, 'avatar':obtenerAvatar(request), 'paginas':{}, 'footer':obtenerFooter(request)})

def verPagina(request, id):
    pagina =Pagina.objects.get(id=id)

    return render(request, 'pagina_individual.html', {'pagina':pagina, 'avatar':obtenerAvatar(request), 'footer':obtenerFooter(request)})

