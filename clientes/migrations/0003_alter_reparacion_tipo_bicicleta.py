# Generated by Django 5.2.2 on 2025-06-10 01:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("clientes", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reparacion",
            name="tipo_bicicleta",
            field=models.CharField(
                choices=[
                    ("Montaña", "Montaña"),
                    ("Ruta", "Ruta"),
                    ("Ciudad", "Ciudad"),
                    ("BMX", "BMX"),
                ],
                max_length=10,
            ),
        ),
    ]
