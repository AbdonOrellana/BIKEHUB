from django.contrib import admin
from .models import Cliente, Bicicleta, Arriendo, Reparacion

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'apellido_materno', 'telefono', 'direccion')  # Campos a mostrar en la lista
    search_fields = ('email', 'first_name', 'last_name', 'telefono')  # Campos por los cuales se puede buscar
    list_filter = ('is_active', 'is_staff')  # Filtros que puedes aplicar en la barra lateral
    ordering = ('email',)  # Orden predeterminado de la lista
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información Personal', {'fields': ('first_name', 'last_name', 'apellido_materno', 'telefono', 'direccion')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
    )

@admin.register(Bicicleta)
class BicicletaAdmin(admin.ModelAdmin):
    list_display = ['marca', 'modelo', 'tipo', 'stock']
    search_fields = ['marca', 'modelo']

@admin.register(Arriendo)
class ArriendoAdmin(admin.ModelAdmin):
    list_display = ['cliente','bicicleta', 'fecha_inicio', 'fecha_fin', 'estado', 'costo_total']
    search_fields = ['bicicleta', 'estado']

@admin.register(Reparacion)
class ReparacionAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'marca_bicicleta', 'tipo_bicicleta', 'descripcion_problema', 'reserva_tecnico']
    search_fields = ['marca_bicicleta', 'tipo_bicicleta', 'descripcion_problema', 'cliente__username']
    list_filter = ['tipo_bicicleta', 'reserva_tecnico__tecnico']