from django.db import models
from django.conf import settings

class Tecnico(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    TIPO_ESPECIALIDAD_CHOICES=[        ('Montaña', 'Montaña'),
        ('Ruta', 'Ruta'),
        ('Ciudad', 'Ciudad'),
        ('BMX', 'BMX'),]
    especialidad = models.CharField( max_length=10, 
    choices=TIPO_ESPECIALIDAD_CHOICES)
    experiencia = models.PositiveIntegerField(default=0)  # Años de experiencia

    def __str__(self):
        return f"{self.nombre} - {self.especialidad}"

class ReservaTecnico(models.Model):
    tecnico = models.ForeignKey(Tecnico, on_delete=models.CASCADE, related_name='reservas')
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    esta_disponible = models.BooleanField(default=True)
    tipo_trabajo = models.CharField(max_length=200, null=True, blank=True)  # Descripción del trabajo asignado

    def __str__(self):
        disponibilidad = "Disponible" if self.esta_disponible else "No Disponible"
        return f"{self.tecnico.nombre} - {self.fecha_inicio.strftime('%Y-%m-%d %H:%M')} a {self.fecha_fin.strftime('%Y-%m-%d %H:%M')} - {disponibilidad}"

class Vendedor(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    fecha_contratacion = models.DateField(null=True, blank=True)  # Fecha en que se unió al equipo

    def __str__(self):
        return self.nombre

class Inventario(models.Model):
    bicicleta = models.ForeignKey('clientes.Bicicleta', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.bicicleta.marca} {self.bicicleta.modelo} - {self.cantidad} unidades"

    def actualizar_stock(self, cantidad_vendida):
        self.cantidad -= cantidad_vendida
        self.save()


class Venta(models.Model):
    vendedor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    cliente_rut = models.CharField(max_length=12, blank=True, null=True)
    numero_venta = models.CharField(max_length=255, unique=True, blank=True, editable=False)
    total = models.DecimalField(max_digits=10, decimal_places=0, default=0, editable=False)

    def save(self, *args, **kwargs):
        if not self.id:  # Si es una nueva instancia y aún no tiene ID
            super(Venta, self).save(*args, **kwargs)  # Primero guarda para obtener un ID
            self.numero_venta = f"VN{self.id:010d}"  # Formato del número de venta, por ejemplo 'VN0000001234'
        super(Venta, self).save(*args, **kwargs)  # Guarda nuevamente con el número de venta actualizado

    def __str__(self):
        return f"Venta {self.numero_venta} - Total: ${self.total}"

class VentaDetalle(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    bicicleta = models.ForeignKey('clientes.Bicicleta', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=0)

    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.bicicleta.precio_venta
        super().save(*args, **kwargs)