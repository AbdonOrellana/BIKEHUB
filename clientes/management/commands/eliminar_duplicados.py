from django.core.management.base import BaseCommand
from django.db.models import Count
from clientes.models import Cliente

class Command(BaseCommand):
    help = 'Elimina registros duplicados de clientes'

    def handle(self, *args, **options):
        # Obteniendo los emails duplicados con un conteo de cuántas veces cada uno aparece
        duplicates = Cliente.objects.values('email').annotate(email_count=Count('email')).filter(email_count__gt=1)

        # Eliminar todos los registros duplicados
        for duplicate in duplicates:
            Cliente.objects.filter(email=duplicate['email']).delete()

        self.stdout.write(self.style.SUCCESS('Registros duplicados eliminados exitosamente'))