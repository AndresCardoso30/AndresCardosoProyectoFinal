from django.shortcuts import render, HttpResponse, redirect
from AppUsuarios.models import *
from AppUsuarios.forms import *
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth import get_user_model
from itertools import chain
from operator import attrgetter

def registro(request):

    if request.method == "POST":

        form = RegistroUsuarioForm(request.POST)
        
        if form.is_valid():

            username = form.cleaned_data['username']
            #password1 = form.cleaned_data['password1']
            #password2 = form.cleaned_data['password2']
            #email = form.cleaned_data['email']
            form.save()
            return render(request, 'inicio.html', {"mensaje": "Usuario creado correctamente"})
        
    else: 

        form = RegistroUsuarioForm()

    return render (request, "registro_usuario.html", {"form": form})


def login_request(request):

    if request.method == "POST":
        form= AuthenticationForm(request, data = request.POST)

        if form.is_valid():
            usuario=form.cleaned_data.get('username')
            contrasena=form.cleaned_data.get('password')

            user=authenticate(username=usuario, password=contrasena)

            if user is not None:
                login(request, user)

                return render(request, 'inicio.html', {"mensaje":f"Bienvenido {usuario}"})
            
            else:

                return render(request, 'login.html', {"mensaje":"Datos ingresados incorrectos"})
            
        else:

            return render(request, "login.html", {"mensaje": "Error, formulario erroneo", "form":form})
        
    form = AuthenticationForm()

    return render(request, "login.html", {"form":form})


@login_required
def editarPerfil(request):

    usuario = request.user

    if request.method == 'POST':
        miFormulario = UserEditForm(request.POST)

        if miFormulario.is_valid:

            informacion = miFormulario.cleaned_data

            usuario.email = informacion['email']
            usuario.password1 = informacion['password1']
            usuario.password2 = informacion['password2']
            usuario.save()

            return render(request, 'inicio.html')
    
    else:

        miFormulario = UserEditForm(initial={'email':usuario.email})
    
    return render(request, 'editar_perfil.html', {"miFormulario":miFormulario, "usuario":usuario})


@login_required
def mostrar_perfiles(request):
    User = get_user_model()
    users = User.objects.all()

    return render(request, "mostrar_perfiles.html", {"users":users})


@login_required
def chatear(request, id):
    emisor = request.user
    receptor = User.objects.get(id=id)
    chats = Mensaje.objects.filter(clave1__icontains=emisor.id).filter(clave2__icontains=receptor.id)
    chats_receptor = Mensaje.objects.filter(clave1__icontains=receptor.id).filter(clave2__icontains=emisor.id)

    resultado = sorted(chain(chats, chats_receptor), key=attrgetter('tiempo'))

    clave1=emisor.id
    clave2=receptor.id   

    if chats:
        mensaje=f"Chats con {receptor.username}"
    else:
        mensaje="No hay chats"

    if request.method == "POST":
        
        miFormulario = MensajeForm(request.POST, initial={'emisor':emisor, 'receptor':receptor, 'clave1':clave1, 'clave2':clave2})

        if miFormulario.is_valid():
            informacion = miFormulario.cleaned_data
            chat=Mensaje(emisor=informacion['emisor'], receptor=informacion['receptor'], mensaje=informacion['mensaje'], clave1=informacion['clave1'], clave2=informacion['clave2'])
            chat.save()
            chats = Mensaje.objects.filter(clave1__icontains=emisor.id).filter(clave2__icontains=receptor.id)
            chats_receptor = Mensaje.objects.filter(clave1__icontains=receptor.id).filter(clave2__icontains=emisor.id)
            resultado = sorted(chain(chats, chats_receptor), key=attrgetter('tiempo'))
            
            
            

            return render(request, "chat.html", {"miFormulario":miFormulario, "chats":resultado, "mensaje":mensaje})
        
    mensaje2= "Algo anda mal..."

    miFormulario = MensajeForm(initial={'emisor':emisor, 'receptor':receptor, 'clave1':clave1, 'clave2':clave2})

    return render(request, "chat.html", {"miFormulario":miFormulario, "mensaje":mensaje, "mensaje2":mensaje2, "chats":resultado})
