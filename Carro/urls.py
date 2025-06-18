# Carro/urls.py (Versión corregida)

from django.urls import path
from . import views

app_name = 'Carro' # Es buena práctica añadir el app_name para los namespaces

urlpatterns = [
    path('agregar_a_carrito/<int:bicicleta_id>/', views.agregar_a_carrito, name='agregar_a_carrito'),
    path('checkout/', views.checkout, name='checkout'),
    path('actualizar_carrito/<int:item_id>/', views.actualizar_carrito, name='actualizar_carrito'),
    path('eliminar_de_carrito/<int:item_id>/', views.eliminar_de_carrito, name='eliminar_de_carrito'),
    path('procesar_pago/', views.procesar_pago, name='procesar_pago'),
]