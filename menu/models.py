from django.db import models
from django.core.validators import MinValueValidator, RegexValidator


solo_letras = RegexValidator(
    regex=r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$',
    message="El nombre solo puede contener letras y espacios."
)

class Plato(models.Model):
    nombre = models.CharField(
        max_length=100,
        validators=[solo_letras]
    )
    descripcion = models.TextField(blank=True)
    precio = models.IntegerField(
        validators=[MinValueValidator(1, message="El precio debe ser mayor que 0.")]
    )
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre