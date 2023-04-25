from django.db import models
from django.contrib.auth.models import User


class Pagina(models.Model):
    titulo=models.CharField(max_length=50)
    subtitulo=models.CharField(max_length=50)
    cuerpo=models.CharField(max_length=1500)
    autor=models.ForeignKey(User, on_delete=models.CASCADE)
    fecha=models.DateTimeField(auto_now_add=True)
    imagen=models.ImageField(upload_to='avatars', null=True, blank=True)

    def __str__(self):
        return f"{self.titulo}--{self.autor}--{self.fecha.day}/{self.fecha.month}/{self.fecha.year}"
    
