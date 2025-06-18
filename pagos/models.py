from django.db import models
from django.conf import settings
from Carro.models import ItemCarro, Orden

class Pago(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('completado', 'Completado'),
        ('fallido', 'Fallido'),
    ]

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items_carro = models.ManyToManyField(ItemCarro)
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_payment_id = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE, null=True, blank=True, related_name='pagos')

    def __str__(self):
        return f"Pago {self.id} - {self.usuario.username} - {self.monto_total}"

    class Meta:
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'
