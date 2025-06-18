from django.urls import path
from . import views
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/home', permanent=False)),
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('arriendo/', views.arriendo, name='arriendo'),
    path('pagar-arriendo/<int:arriendo_id>/', views.pagar_arriendo, name='pagar_arriendo'),
    path('orden_arriendo/<int:orden_id>/', views.orden_arriendo, name='orden_arriendo'),
    path('home/', views.home, name='home'), # Asumiendo que tienes una vista 'home' o la ruta raíz.
    path('reparacion/', views.reparacion, name='reparacion'),
    path('reparacion_exito/', views.reparacion_exito, name='reparacion_exito'),
    path('catalogo/', views.catalogo_bicicletas, name='catalogo_bicicletas'),
    path('bicicletas/<int:id>/', views.detalles_bicicleta, name='detalles_bicicleta'),
    path('buscar_bicicletas/', views.buscar_bicicletas, name='buscar_bicicletas'),
    path('ordenes/', views.ver_todas_ordenes, name='ver_ordenes'),
]