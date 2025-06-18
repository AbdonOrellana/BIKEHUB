from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from clientes.models import Bicicleta

class ItemCarro(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='items_carro')
    bicicleta = models.ForeignKey(Bicicleta, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cantidad} de {self.bicicleta}"

class Orden(models.Model):
    ESTADO_CHOICES = [
        ('Pendiente de Pago', 'Pendiente de Pago'),
        ('Procesando Pedido', 'Procesando'),
        ('Pedido Confirmado', 'Confirmado'),
        ('Enviado', 'Enviado'),
        ('Entregado', 'Entregado'),
        ('Cancelado', 'Cancelado')  # Asegúrate de añadir este estado si aún no existe
    ]
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ordenes')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Procesando Pedido')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f'Orden {self.id} - {self.estado}'

    def update_total(self):
        self.total = sum(item.precio * item.cantidad for item in self.items.all())
        self.save()
        
    def cancelar_orden(self):
        if self.estado not in ['Entregado', 'Cancelado']:  # Asumiendo que no se pueden cancelar órdenes ya entregadas
            for item in self.items.all():
                item.bicicleta.incrementar_stock(item.cantidad)
            self.estado = 'Cancelado'
            self.save()
            return True
        return False

class OrdenItem(models.Model):
    orden = models.ForeignKey(Orden, related_name='items', on_delete=models.CASCADE)
    bicicleta = models.ForeignKey(Bicicleta, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.cantidad} x {self.bicicleta} a {self.precio}'
    
@receiver([post_save, post_delete], sender=OrdenItem)
def update_order_total(sender, instance, **kwargs):
    instance.orden.update_total()