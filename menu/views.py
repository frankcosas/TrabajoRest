from django.shortcuts import render, redirect, get_object_or_404
from .models import Plato
from .forms import PlatoForm

# Página principal (Home)
def home(request):
    return render(request, 'menu/home.html')

# Listado de platos
def lista_platos(request):
    platos = Plato.objects.all()
    return render(request, 'menu/lista_platos.html', {'platos': platos})

# Formulario para crear
def crear_plato(request):
    if request.method == 'POST':
        form = PlatoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_platos')
    else:
        form = PlatoForm()
    return render(request, 'menu/crear_plato.html', {'form': form})

# Formulario para editar
def editar_plato(request, pk):
    plato = get_object_or_404(Plato, pk=pk)
    if request.method == 'POST':
        form = PlatoForm(request.POST, instance=plato)
        if form.is_valid():
            form.save()
            return redirect('lista_platos')
    else:
        form = PlatoForm(instance=plato)
    return render(request, 'menu/editar_plato.html', {'form': form, 'plato': plato})

# Eliminar plato
def eliminar_plato(request, pk):
    plato = get_object_or_404(Plato, pk=pk)
    if request.method == 'POST':
        plato.delete()
        return redirect('lista_platos')
    return render(request, 'menu/eliminar_plato.html', {'plato': plato})