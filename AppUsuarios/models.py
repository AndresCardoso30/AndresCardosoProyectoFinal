from django.db import models
from django.contrib.auth.models import User

class Mensaje(models.Model):
    
    emisor = models.CharField(max_length=30)
    receptor=models.CharField(max_length=30)
    mensaje = models.CharField(max_length=200)
    tiempo = models.DateTimeField(auto_now_add=True)
    clave1= models.CharField(max_length=100)
    clave2= models.CharField(max_length=100) 
   
    

    def __str__(self):
        return f"{self.mensaje} -- {self.emisor}"
    

class Avatar(models.Model):
    imagen= models.ImageField(upload_to='avatars', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.imagen
    
class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre=models.CharField(max_length=30)
    apellido=models.CharField(max_length=30)
    biografia=models.CharField(max_length=1500)
    imagen=models.ImageField(upload_to='perfiles', null=True, blank=True)


