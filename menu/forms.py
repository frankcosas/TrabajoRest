from django import forms
from .models import Plato

class PlatoForm(forms.ModelForm):
    class Meta:
        model = Plato
        fields = ['nombre', 'descripcion', 'precio', 'disponible']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Lomo a lo Pobre',
                'required': 'required',
                'pattern': r'[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+',
                'title': 'El nombre solo puede contener letras y espacios'
            }),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción del plato'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 12000', 'min': '1', 'required': 'required'}),
            'disponible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        # Verifica que contenga al menos una letra y no sean solo dígitos o caracteres especiales
        if nombre and not any(c.isalpha() for c in nombre):
            raise forms.ValidationError("El nombre debe contener letras válidas.")
        return nombre

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio is None or precio <= 0:
            raise forms.ValidationError("El precio debe ser un número positivo mayor que 0.")
        return precio