from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from AppUsuarios.models import *
 


class RegistroUsuarioForm(UserCreationForm):
    email=forms.EmailField(label="Email usuario")
    password1=forms.CharField(label="Contrasena", widget=forms.PasswordInput)
    password2=forms.CharField(label="Confirmar contrasena", widget=forms.PasswordInput)
    

    class Meta:
        model=User
        fields=["username", "email", "password1", "password2"]
        help_texts= {k:"" for k in fields}



class UserEditForm(forms.ModelForm):
    email = forms.EmailField(label="Modificar email")
    password1 = forms.CharField(label="Contrasena", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmar contrasena", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']
        help_texts= {k:"" for k in fields}

class MensajeForm(forms.Form):
    emisor = forms.CharField(max_length=30)
    receptor = forms.CharField(max_length=30)
    mensaje = forms.CharField(label="Mensaje", max_length=200)
    clave1=forms.CharField(max_length=100, widget=forms.HiddenInput)
    clave2=forms.CharField(max_length=100, widget=forms.HiddenInput)

    class Meta:
        model=Mensaje

class AvatarFormulario(forms.Form):
    imagen=forms.ImageField(label='Imagen')


class PerfilForm(forms.Form):
    nombre=forms.CharField(max_length=30)
    apellido=forms.CharField(max_length=30)
    biografia=forms.CharField(max_length=1500)
    imagen=forms.ImageField(label='Imagen de perfil', required=False)

    class Meta:
        model=Perfil


