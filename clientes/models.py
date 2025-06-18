from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class Cliente(AbstractUser):
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    apellido_materno = models.CharField(max_length=30, null=True, blank=True)
    telefono = models.CharField(max_length=15, null=True, blank=True)
    direccion = models.TextField(null=True, blank=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'apellido_materno']

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)

class Bicicleta(models.Model):
    TIPO_CHOICES = [
        ('Montaña', 'Montaña'),
        ('Ruta', 'Ruta'),   
        ('Ciudad', 'Ciudad'),
        ('BMX', 'BMX')
    ]
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES)
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='bicicletas/', null=True, blank=True)
    precio_por_dia = models.IntegerField(default=0, null=True, blank=True)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    stock = models.IntegerField(default=0)
    disponible_para_venta = models.BooleanField(default=False)
    disponible_para_arriendo = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.tipo}) "
    
    def incrementar_stock(self, cantidad):
        self.stock += cantidad
        self.save()

    def decrementar_stock(self, cantidad):
        if self.stock >= cantidad:
            self.stock -= cantidad
            self.actualizar_disponibilidad()
            self.save()
        else:
            raise ValueError("Stock insuficiente")

    def actualizar_disponibilidad(self):
        """Actualizar la disponibilidad basada en el stock actual."""
        if self.stock <= 0:
            self.disponible_para_venta = False
            self.disponible_para_arriendo = False
        else:
            self.disponible_para_venta = True  # Puede personalizarse más según las reglas de negocio
            self.disponible_para_arriendo = True
        self.save()

class Arriendo(models.Model):
    id = models.AutoField(primary_key=True)  # Agrega un campo ID que se incrementa automáticamente
    cliente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bicicleta = models.ForeignKey('Bicicleta', on_delete=models.SET_NULL, null=True)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    forma_pago = models.CharField(max_length=20, choices=[
        ('Debito', 'Débito'),
        ('Credito', 'Crédito'),
        ('Transferencia', 'Transferencia Bancaria')
    ])
    costo_arriendo = models.IntegerField(default=0)
    deposito_garantia = models.IntegerField(default=100000)
    costo_total = models.IntegerField(default=0)
    
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('completado', 'Completado')
    ]
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')

    def __str__(self):
        return f"Arriendo {self.id} - {self.cliente.username} - {self.bicicleta.modelo}"
    
    def save(self, *args, **kwargs):
        self.costo_total = self.costo_arriendo + self.deposito_garantia
        super().save(*args, **kwargs)

class Reparacion(models.Model):
    TIPO_BICICLETA_CHOICES = [
        ('Montaña', 'Montaña'),
        ('Ruta', 'Ruta'),
        ('Ciudad', 'Ciudad'),
        ('BMX', 'BMX'),
    ]
    
    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='reparaciones'
    )
    marca_bicicleta = models.CharField(max_length=100)
    tipo_bicicleta = models.CharField(
        max_length=10, 
        choices=TIPO_BICICLETA_CHOICES
    )
    descripcion_problema = models.TextField()
    reserva_tecnico = models.ForeignKey(
        'tecnicos_vendedores.ReservaTecnico', 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='reparaciones'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    TIPO_ESTADO_CHOICES = [
        ('Esperando producto.', 'Esperando Producto'),
        ('En reparacion', 'En Reparacion'),
        ('Listo para retirar', 'Listo para el Retiro'),
    ]
    estado_reparacion = models.CharField(
        max_length=25,
        choices=TIPO_ESTADO_CHOICES
    )
    def __str__(self):
        return f"{self.marca_bicicleta} {self.get_tipo_bicicleta_display()} - {self.cliente}"

    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = 'Reparación'
        verbose_name_plural = 'Reparaciones'