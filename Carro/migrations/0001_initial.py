# Generated by Django 5.2.2 on 2025-06-05 00:16

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ItemCarro",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("cantidad", models.PositiveIntegerField(default=1)),
                ("fecha_agregado", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Orden",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("fecha_creacion", models.DateTimeField(auto_now_add=True)),
                ("fecha_actualizacion", models.DateTimeField(auto_now=True)),
                (
                    "estado",
                    models.CharField(
                        choices=[
                            ("Procesando Pedido", "Procesando"),
                            ("Pedido Confirmado", "Confirmado"),
                            ("Enviado", "Enviado"),
                            ("Entregado", "Entregado"),
                            ("Cancelado", "Cancelado"),
                        ],
                        default="Procesando Pedido",
                        max_length=20,
                    ),
                ),
                (
                    "total",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
            ],
        ),
        migrations.CreateModel(
            name="OrdenItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("precio", models.DecimalField(decimal_places=2, max_digits=10)),
                ("cantidad", models.PositiveIntegerField(default=1)),
            ],
        ),
    ]
