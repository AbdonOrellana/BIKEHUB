from pyexpat.errors import messages
from django.contrib import admin
from .models import Orden, OrdenItem

class OrdenItemInline(admin.TabularInline):
    model = OrdenItem
    extra = 0
    fields = ('bicicleta', 'cantidad', 'precio')
    readonly_fields = ('bicicleta', 'cantidad', 'precio')

class OrdenAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'estado', 'fecha_creacion', 'total')
    list_filter = ('estado', 'fecha_creacion')
    search_fields = ('usuario__username', 'estado')
    readonly_fields = ('usuario','estado','fecha_creacion', 'fecha_actualizacion', 'total')
    inlines = [OrdenItemInline]
    actions = ['cancelar_pedidos']

    def cancelar_pedidos(self, request, queryset):
        for orden in queryset:
            if orden.cancelar_orden():
                self.message_user(request, f'Orden {orden.id} cancelada y stock restaurado.')
            else:
                self.message_user(request, f'Orden {orden.id} no se pudo cancelar.', level=messages.ERROR)
    cancelar_pedidos.short_description = "Cancelar pedidos seleccionados y restaurar stock"

admin.site.register(Orden, OrdenAdmin)
