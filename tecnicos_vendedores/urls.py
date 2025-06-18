from django.urls import path
from . import views

urlpatterns = [
    path('agregar_bicicleta/', views.agregar_bicicleta, name='agregar_bicicleta'),
    path('gestion_inventario/', views.gestion_inventario, name='gestion_inventario'),
    path('gestion_bicicletas/', views.gestion_bicicletas_view, name='gestion_bicicletas'),
    path('inventario_exito/', views.inventario_exito_view, name='inventario_exito'),
    path('registrar_venta/', views.registrar_venta, name='registrar_venta'),
    path('venta_exito/', views.venta_exito_view, name='venta_exito'),
]