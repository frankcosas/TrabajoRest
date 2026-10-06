from django.db import models

class Plato(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.IntegerField()
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
        
