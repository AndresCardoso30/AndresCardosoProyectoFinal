from django import forms

class PaginaForm(forms.Form):
    titulo=forms.CharField(max_length=50)
    subtitulo=forms.CharField(max_length=200)
    cuerpo=forms.CharField(max_length=1500)
    imagen=forms.ImageField(label='Imagen')