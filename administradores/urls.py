from django.urls import path
from . import views

urlpatterns = [
    path('ganancias_semanales/', views.ganancias_semanales, name='ganancias_semanales'),
    path('ganancias_mensuales/', views.ganancias_mensuales, name='ganancias_mensuales'),
    path('admin_dashboard/', views.dashboard, name='admin_dashboard'),
    path('registrar_tecnicos/', views.registrar_tecnico, name='registrar_tecnico'),
    path('registrar_vendedores/', views.registrar_vendedor, name='registrar_vendedor'),
]