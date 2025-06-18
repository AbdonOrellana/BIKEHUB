from django.urls import path
from . import views

app_name = 'pagos'

urlpatterns = [
    path('procesar/', views.procesar_pago, name='procesar_pago'),
    path('crear-pago/', views.crear_pago, name='crear_pago'),
    path('crear_pago_arriendo/', views.crear_pago_arriendo, name='crear_pago_arriendo'),
    path('confirmar-pago-exitoso/', views.confirmar_pago_exitoso, name='confirmar_pago_exitoso'),
    path('exito/', views.exito, name='exito'),
    path('webhook/', views.webhook_stripe, name='webhook_stripe'),
] 