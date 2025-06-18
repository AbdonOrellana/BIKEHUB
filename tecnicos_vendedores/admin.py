from django.contrib import admin
from django.utils.timezone import make_aware
from datetime import datetime, timedelta, time
from .models import Tecnico, ReservaTecnico

@admin.action(description='Generar horarios para técnicos seleccionados')
def generar_horarios(modeladmin, request, queryset):
    for tecnico in queryset:
        # Asigna horarios de trabajo desde las 9 AM hasta las 5 PM
        for i in range(5):  # Suponiendo que se generen horarios para 5 días desde hoy
            fecha = datetime.now().date() + timedelta(days=i)
            # Solo días de semana (lunes a viernes)
            if fecha.weekday() < 5:
                inicio = make_aware(datetime.combine(fecha, time(9, 0)))  # Inicio a las 9 AM
                fin = inicio
                while fin.time() < time(17, 0):  # Hasta las 5 PM
                    fin = inicio + timedelta(hours=2)
                    ReservaTecnico.objects.create(tecnico=tecnico, fecha_inicio=inicio, fecha_fin=fin, esta_disponible=True)
                    inicio = fin
    modeladmin.message_user(request, "Horarios generados correctamente para los técnicos seleccionados.")

class ReservaTecnicoAdmin(admin.ModelAdmin):
    list_display = ['tecnico', 'fecha_inicio', 'fecha_fin', 'esta_disponible']
    actions = [generar_horarios]

class TecnicoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'especialidad']
    actions = [generar_horarios]

admin.site.register(Tecnico, TecnicoAdmin)
admin.site.register(ReservaTecnico, ReservaTecnicoAdmin)

from django.contrib import admin
from .models import Venta, VentaDetalle

class VentaDetalleInline(admin.TabularInline):
    model = VentaDetalle
    extra = 1  # Número de formas vacías para detalles de venta a mostrar por defecto

class VentaAdmin(admin.ModelAdmin):
    list_display = ('numero_venta', 'vendedor', 'fecha', 'cliente_rut', 'total')  # Campos a mostrar en la lista
    inlines = [VentaDetalleInline]  # Integrar detalles de venta directamente en la página de venta

admin.site.register(Venta, VentaAdmin)