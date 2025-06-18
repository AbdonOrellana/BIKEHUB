from django.contrib import admin
from .models import Pago

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'orden', 'monto_total', 'estado', 'fecha_creacion')
    list_filter = ('estado', 'fecha_creacion')
    search_fields = ('usuario__username', 'stripe_payment_id')
    readonly_fields = ('stripe_payment_id', 'fecha_creacion', 'fecha_actualizacion')
