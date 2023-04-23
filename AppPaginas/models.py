from django.db import models


class Pagina(models.Model):
    titulo=models.CharField(max_length=50)
    subtitulo=models.CharField(max_length=50)
    cuerpo=models.CharField(max_length=1500)
    autor=models.CharField(max_length=50)
    fecha=models.DateTimeField(auto_now_add=True)
    imagen=models.ImageField()

    def __str__(self):
        return f"{self.titulo}--{self.autor}--{self.fecha.day}/{self.fecha.month}/{self.fecha.year}"
    
