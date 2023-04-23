from django import forms

class PaginaForm(forms.Form):
    titulo=forms.CharField(max_length=50)
    subtitulo=forms.CharField(max_length=50)
    cuerpo=forms.CharField(max_length=1500)
    autor=forms.CharField(max_length=50)
    imagen=forms.ImageField()