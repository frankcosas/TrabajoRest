from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('platos/', views.lista_platos, name='lista_platos'),
    path('platos/crear/', views.crear_plato, name='crear_plato'),
    path('platos/editar/<int:pk>/', views.editar_plato, name='editar_plato'),
    path('platos/eliminar/<int:pk>/', views.eliminar_plato, name='eliminar_plato'),
]