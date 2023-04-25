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

def obtenerFooter(request):
    
    return "/media/varios/abajo.png"

def registro(request):

    if request.method == "POST":

        form = RegistroUsuarioForm(request.POST)
        
        if form.is_valid():

            username = form.cleaned_data['username']
            #password1 = form.cleaned_data['password1']
            #password2 = form.cleaned_data['password2']
            #email = form.cleaned_data['email']
            form.save()
            return render(request, 'inicio.html', {"mensaje": "Usuario creado correctamente", 'avatar':obtenerAvatar(request), 'footer':obtenerFooter(request)})
        
    else: 

        form = RegistroUsuarioForm()

    return render (request, "registro_usuario.html", {"form": form, 'avatar':obtenerAvatar(request), 'footer':obtenerFooter(request)})


def login_request(request):

    if request.method == "POST":
        form= AuthenticationForm(request, data = request.POST)

        if form.is_valid():
            usuario=form.cleaned_data.get('username')
            contrasena=form.cleaned_data.get('password')

            user=authenticate(username=usuario, password=contrasena)

            if user is not None:
                login(request, user)

                return render(request, 'inicio.html', {"mensaje":f"Bienvenido {usuario}", 'avatar':obtenerAvatar(request), 'footer':obtenerFooter(request)})
            
            else:

                return render(request, 'login.html', {"mensaje":"Datos ingresados incorrectos", 'avatar':obtenerAvatar(request), 'footer':obtenerFooter(request)})
            
        else:

            return render(request, "login.html", {"mensaje": "Error, formulario erroneo", "form":form, 'avatar':obtenerAvatar(request), 'footer':obtenerFooter(request)})
        
    form = AuthenticationForm()

    return render(request, "login.html", {"form":form, 'avatar':obtenerAvatar(request), 'footer':obtenerFooter(request)})


@login_required
def editarPerfil(request):

    usuario = request.user
    perfil = Perfil.objects.all()

    if request.method == 'POST':
        miFormulario = UserEditForm(request.POST)

        if miFormulario.is_valid():

            informacion = miFormulario.cleaned_data
            
            usuario.username = informacion['username']
            usuario.email = informacion['email']
            usuario.password1 = informacion['password1']
            usuario.password2 = informacion['password2']
            usuario.save()
            mensaje = "Usuario actualizado de forma correcta."

            return render(request, 'inicio.html', {'mensaje': mensaje, 'avatar':obtenerAvatar(request), 'footer':obtenerFooter(request), 'user':usuario, 'perfil':perfil})
    
    else:

        miFormulario = UserEditForm(initial={'email':usuario.email})
    
    return render(request, 'editar_perfil.html', {"miFormulario":miFormulario, "usuario":usuario, 'avatar':obtenerAvatar(request), 'footer':obtenerFooter(request)})


@login_required
def mostrar_perfiles(request):
    User = get_user_model()
    users = User.objects.all()
   
    

    return render(request, "mostrar_perfiles.html", {"users":users, 'avatar':obtenerAvatar(request), 'footer':obtenerFooter(request)})




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
            
            
            

            return render(request, "chat.html", {"miFormulario":miFormulario, "chats":resultado, "mensaje":mensaje, 'emisor':emisor, 'avatar':obtenerAvatar(request), 'footer':obtenerFooter(request)})
        
    mensaje2= "Algo anda mal..."

    miFormulario = MensajeForm(initial={'emisor':emisor, 'receptor':receptor, 'clave1':clave1, 'clave2':clave2})

    return render(request, "chat.html", {"miFormulario":miFormulario, "mensaje":mensaje, "mensaje2":mensaje2, "chats":resultado, 'emisor':emisor, 'avatar':obtenerAvatar(request), 'footer':obtenerFooter(request)})

def obtenerAvatar(request):
    avatares=Avatar.objects.filter(user=request.user.id)

    if len(avatares)!=0:
        return avatares[0].imagen.url
    else: 
        return "/media/avatars/default.png"
    


@login_required
def agregarAvatar(request):
    if request.method == 'POST':

        form = AvatarFormulario(request.POST, request.FILES)

        if form.is_valid():
            u = User.objects.get(username=request.user)

            avatar = Avatar (user=u, imagen=form.cleaned_data['imagen'])
            avatarViejo = Avatar.objects.filter(user=request.user)
            if len(avatarViejo)>0:
                avatarViejo[0].delete()
            avatar.save()
            mensaje = 'Avatar agregado correctamente'

            return render(request, 'inicio.html', {'avatar':obtenerAvatar(request), 'mensaje':mensaje, 'footer':obtenerFooter(request)})

        else: 
            return render(request, 'agregarAvatar.html', {'form':form, 'mensaje': "Error en el formulario", 'avatar':obtenerAvatar(request), 'footer':obtenerFooter(request)})
    else:
        form = AvatarFormulario()
        return render(request, 'agregarAvatar.html', {'form':form, 'avatar':obtenerAvatar(request), 'footer':obtenerFooter(request)})
    


@login_required
def agregarPerfil(request):
    if request.method == 'POST':

        form = PerfilForm(request.POST, request.FILES)

        if form.is_valid():
            u = User.objects.get(username=request.user)

            perfil = Perfil (user=u, nombre=form.cleaned_data['nombre'], apellido=form.cleaned_data['apellido'], biografia=form.cleaned_data['biografia'], imagen=form.cleaned_data['imagen'])
            
            perfil.save()
            mensaje = 'Perfil agregado correctamente'

            return render(request, 'ver_perfil_individual.html', {'avatar':obtenerAvatar(request), 'mensaje':mensaje, 'footer':obtenerFooter(request), 'perfil':perfil})

        else: 
            return render(request, 'agregar_perfil.html', {'form':form, 'mensaje': "Error en el formulario", 'avatar':obtenerAvatar(request), 'footer':obtenerFooter(request)})
    else:
        form = PerfilForm()
        return render(request, 'agregar_perfil.html', {'form':form, 'avatar':obtenerAvatar(request), 'footer':obtenerFooter(request)})

@login_required    
def verPerfil(request, id):
   u = User.objects.get(id=id)
   perfil = Perfil.objects.all()
   
   if perfil:
       return render(request, 'ver_perfil_individual.html', {'avatar':obtenerAvatar(request), 'footer':obtenerFooter(request), 'user':u, 'perfil':perfil}) 
   else:
       return render(request, 'ver_perfil_individual.html', {'avatar':obtenerAvatar(request), 'footer':obtenerFooter(request), 'mensaje':'Usuario no cuenta aun con un perfil.'})

@login_required   
def verMiPerfil(request):
    u = User.objects.get(username=request.user)
    perfil = Perfil.objects.all()
    return render(request, 'ver_perfil_individual.html', {'avatar':obtenerAvatar(request), 'footer':obtenerFooter(request), 'user':u, 'perfil':perfil})

@login_required
def eeditar_mi_perfil(request):

    usuario = request.user
    perfil = Perfil.objects.all()

    if request.method == 'POST':
        form = PerfilForm(request.POST)

        if form.is_valid():
            u = User.objects.get(username=request.user)

           
            imagen=form.cleaned_data['imagen']
            if imagen:
                perfil_u = Perfil (user=u, nombre=form.cleaned_data['nombre'], apellido=form.cleaned_data['apellido'], biografia=form.cleaned_data['biografia'], imagen=form.cleaned_data['imagen'])
            else:
                perfil_u = Perfil (user=u, nombre=form.cleaned_data['nombre'], apellido=form.cleaned_data['apellido'], biografia=form.cleaned_data['biografia'])
            perfil_u.save()
            mensaje = 'Perfil actualizado correctamente'

            return render(request, 'ver_perfil_individual.html', {'avatar':obtenerAvatar(request), 'mensaje':mensaje, 'footer':obtenerFooter(request), 'perfil':perfil_u})

        else: 
            return render(request, 'editar_mi_perfil.html', {'form':form, 'mensaje': "Error en el formulario", 'avatar':obtenerAvatar(request), 'footer':obtenerFooter(request)})
    
    else:

        form = PerfilForm(initial={'nombre':usuario.perfil.nombre, 'apellido':usuario.perfil.apellido, 'biografia':usuario.perfil.biografia, 'imagen':usuario.perfil.imagen})
    
    return render(request, 'editar_mi_perfil.html', {"form":form, "usuario":usuario, 'avatar':obtenerAvatar(request), 'footer':obtenerFooter(request)})

def editar_mi_perfil(request):

    usuario = request.user
    perfil = usuario.perfil

    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES)

        if form.is_valid():

            perfil.nombre = form.cleaned_data['nombre']
            perfil.apellido = form.cleaned_data['apellido']
            perfil.biografia = form.cleaned_data['biografia']
            
            imagen = form.cleaned_data.get('imagen')
            if imagen:
                perfil.imagen = imagen

            perfil.save()

            mensaje = 'Perfil actualizado correctamente'

            return render(request, 'ver_perfil_individual.html', {'avatar':obtenerAvatar(request), 'mensaje':mensaje, 'footer':obtenerFooter(request), 'perfil':perfil})

        else: 
            return render(request, 'editar_mi_perfil.html', {'form':form, 'mensaje': "Error en el formulario", 'avatar':obtenerAvatar(request), 'footer':obtenerFooter(request)})
    
    else:
        form = PerfilForm(initial={'nombre':perfil.nombre, 'apellido':perfil.apellido, 'biografia':perfil.biografia})
    
    return render(request, 'editar_mi_perfil.html', {"form":form, "usuario":usuario, 'avatar':obtenerAvatar(request), 'footer':obtenerFooter(request)})